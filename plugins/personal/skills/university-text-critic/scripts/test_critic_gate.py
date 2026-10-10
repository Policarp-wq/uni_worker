"""Regression checks for approval, stale inputs, and persistent attempt limits."""

from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import critic_gate as gate


def try_begin(source, context):
    try:
        gate.begin(source, context)
        return True
    except gate.GateError:
        return False


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="critic-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "work.md"
        self.source.write_text("# Работа\nШлюз передаёт запрос провайдеру.\n", encoding="utf-8")
        self.context = self.root / ".critic-context.json"
        self.data = {"subject": "ПИС", "topic": "Шлюз", "requirements": ["Описать процесс"],
                     "previous_exists": False, "previous": []}
        self.write_context()

    def write_context(self):
        self.context.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

    def review(self, verdict="approve"):
        ticket = gate.begin(self.source, self.context)
        Path(ticket["report"]).write_text(f"Вердикт: {verdict.upper()}\nПроверено.\n", encoding="utf-8")
        gate.finish(self.source, ticket["ticket"], "test-critic", verdict)
        return ticket

    def test_missing_and_empty_marker(self):
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)
        (self.root / ".critic-approve").touch()
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)

    def test_approval_and_stale_source(self):
        self.review()
        self.assertTrue(gate.require_approval(self.source)["approved"])
        self.source.write_text("Изменённая работа", encoding="utf-8")
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)

    def test_context_and_previous_are_bound(self):
        previous = self.root / "previous.md"
        previous.write_text("Предыдущая работа", encoding="utf-8")
        self.data.update(previous_exists=True, previous=["previous.md"])
        self.write_context()
        self.review()
        original = previous.read_text(encoding="utf-8")
        previous.write_text("Правка предыдущей", encoding="utf-8")
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)
        previous.write_text(original, encoding="utf-8")
        self.data["topic"] = "Другая тема"
        self.write_context()
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)

    def test_invalid_context_does_not_consume_attempt(self):
        self.data.update(previous_exists=True)
        self.write_context()
        with self.assertRaises(gate.GateError):
            gate.begin(self.source, self.context)
        self.data.update(previous_exists=False)
        self.write_context()
        self.assertEqual(gate.begin(self.source, self.context)["attempt"], 1)

    def test_pdf_previous_rejected(self):
        (self.root / "previous.pdf").write_text("not a real PDF", encoding="utf-8")
        self.data.update(previous_exists=True, previous=["previous.pdf"])
        self.write_context()
        with self.assertRaises(gate.GateError):
            gate.begin(self.source, self.context)

    def test_windows_stops_before_creating_review_state(self):
        result = subprocess.run(
            [sys.executable, "-c",
             "import runpy, sys; sys.platform = 'win32'; "
             "runpy.run_path(sys.argv.pop(1), run_name='__main__')",
             gate.__file__, "begin", "--source", str(self.source),
             "--context", str(self.context)],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Windows", result.stderr)
        self.assertIn("fcntl", result.stderr)
        self.assertIn("заменить", result.stderr)
        self.assertFalse((self.root / ".critic-state.json").exists())
        self.assertFalse((self.root / ".critic-lock").exists())

    def test_three_attempts_persist_across_processes(self):
        for i in range(3):
            self.assertEqual(self.review("revise")["attempt"], i + 1)
        result = subprocess.run([sys.executable, gate.__file__, "begin", "--source", str(self.source),
                                 "--context", str(self.context)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("HUMAN_REQUIRED", result.stderr)

    def test_author_resolution_starts_new_cycle_and_preserves_history(self):
        first_cycle = [self.review("revise") for _ in range(3)]
        with self.assertRaises(gate.GateError):
            gate.begin(self.source, self.context)

        resolution = gate.resolve(self.source, "Автор согласовал продолжение")
        self.assertEqual((resolution["cycle"], resolution["attempt"]), (2, 1))
        next_attempt = gate.begin(self.source, self.context)
        self.assertEqual((next_attempt["cycle"], next_attempt["attempt"]), (2, 1))
        self.assertNotEqual(next_attempt["report"], first_cycle[-1]["report"])

        state = json.loads((self.root / ".critic-state.json").read_text(encoding="utf-8"))
        self.assertEqual(len(state["attempts"]), 4)
        self.assertEqual(state["human_resolutions"][0]["decision"], "Автор согласовал продолжение")
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)

    def test_cancel_consumes_attempt_and_pending_blocks(self):
        ticket = gate.begin(self.source, self.context)
        with self.assertRaises(gate.GateError):
            gate.begin(self.source, self.context)
        gate.cancel(self.source, ticket["ticket"], "Агент не запустился")
        self.assertEqual(gate.begin(self.source, self.context)["attempt"], 2)

    def test_change_during_review_and_wrong_ticket(self):
        ticket = gate.begin(self.source, self.context)
        with self.assertRaises(gate.GateError):
            gate.finish(self.source, "wrong", "critic", "approve")
        self.source.write_text("Другая версия", encoding="utf-8")
        with self.assertRaises(gate.GateError):
            gate.finish(self.source, ticket["ticket"], "critic", "approve")
        gate.cancel(self.source, ticket["ticket"], "Текст изменён")

    def test_report_tampering_and_foreign_source(self):
        ticket = self.review()
        Path(ticket["report"]).write_text("Другая рецензия", encoding="utf-8")
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)
        other = self.root / "other.md"
        other.write_bytes(self.source.read_bytes())
        with self.assertRaises(gate.GateError):
            gate.require_approval(other)

    def test_new_attempt_invalidates_old_marker(self):
        self.review()
        gate.begin(self.source, self.context)
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)

    def test_parallel_begin_reserves_once(self):
        with ProcessPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(try_begin, [self.source] * 2, [self.context] * 2))
        self.assertEqual(sum(results), 1)

    def test_corrupt_state_fails_closed(self):
        self.review()
        (self.root / ".critic-state.json").write_text("broken", encoding="utf-8")
        with self.assertRaises(gate.GateError):
            gate.require_approval(self.source)


if __name__ == "__main__":
    unittest.main()
