"""Regression checks for prose metrics, lint and the compression gate."""

from pathlib import Path
import tempfile
import unittest

import prose_gate as prose

SENTENCE = "Шлюз передаёт запрос провайдеру.\n\n"


class ProseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="prose-test-")
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "work.md"
        self.write(SENTENCE * 20)

    def write(self, text):
        self.source.write_text("# Работа\n\n" + text, encoding="utf-8")

    def test_prose_excludes_tables_formulas_code_and_captions(self):
        self.write("Шлюз передаёт запрос.\n\n| a | b |\n| --- | --- |\n| много слов | ещё слова |\n\n"
                   "$$x = y \\tag{1}$$\n\n```\ncode words here\n```\n\nТаблица 1 — Итоги\n\n"
                   "- Провайдер проводит платёж;\n- шлюз хранит $N$ статусов.\n")
        self.assertEqual(prose.measure(self.source)["prose_words"], 9)

    def test_compression_requires_ten_percent(self):
        prose.baseline(self.source)
        self.write(SENTENCE * 19)
        with self.assertRaises(prose.GateError) as error:
            prose.compress(self.source)
        self.assertIn("COMPRESSION_REQUIRED", str(error.exception))
        self.write(SENTENCE * 18)
        result = prose.compress(self.source)
        self.assertEqual((result["result"]["before"], result["result"]["after"]), (80, 72))
        self.assertTrue(prose.require_compression(self.source)["compressed"])

    def test_minimum_cannot_be_lowered(self):
        prose.baseline(self.source)
        with self.assertRaises(prose.GateError):
            prose.compress(self.source, minimum=0.05)

    def test_baseline_cannot_be_rerecorded_in_open_round(self):
        prose.baseline(self.source)
        self.write(SENTENCE * 18)
        with self.assertRaises(prose.GateError):
            prose.baseline(self.source)

    def test_hard_findings_block_compression(self):
        prose.baseline(self.source)
        self.write(SENTENCE * 15 + "Следует отметить, что шлюз хранит статус.\n")
        with self.assertRaises(prose.GateError) as error:
            prose.compress(self.source)
        self.assertIn("hard lint", str(error.exception))

    def test_em_dash_in_prose_is_hard_but_caption_is_exempt(self):
        self.write("Таблица 1 — Итоги\n\nШлюз — посредник.\n")
        findings = prose.measure(self.source)["findings"]
        self.assertEqual([f["rule"] for f in findings if f["hard"]], ["em-dash"])

    def test_waiver_records_human_decision(self):
        prose.baseline(self.source)
        self.write(SENTENCE * 19)
        result = prose.compress(self.source, waive="Текст уже плотный, автор принял 5 %")
        self.assertEqual(result["result"]["waiver"], "Текст уже плотный, автор принял 5 %")
        self.assertTrue(prose.require_compression(self.source)["compressed"])

    def test_regrowth_after_compression_is_blocked(self):
        prose.baseline(self.source)
        self.write(SENTENCE * 18)
        prose.compress(self.source)
        self.write(SENTENCE * 19)
        with self.assertRaises(prose.GateError):
            prose.require_compression(self.source)
        prose.baseline(self.source)
        self.write(SENTENCE * 17)
        prose.compress(self.source)
        self.assertTrue(prose.require_compression(self.source)["compressed"])

    def test_missing_or_forged_marker_fails(self):
        with self.assertRaises(prose.GateError):
            prose.require_compression(self.source)
        prose.baseline(self.source)
        self.write(SENTENCE * 18)
        prose.compress(self.source)
        marker = self.source.parent / ".compress-approve"
        marker.write_text("{}", encoding="utf-8")
        with self.assertRaises(prose.GateError):
            prose.require_compression(self.source)

    def test_long_sentence_and_process_narration(self):
        long = " ".join(["слово"] * 45) + ".\n\n"
        self.write(long + "Схему нарисовал скрипт.\n")
        rules = {(f["rule"], f["hard"]) for f in prose.measure(self.source)["findings"]}
        self.assertIn(("long-sentence", True), rules)
        self.assertIn(("process-narration", False), rules)


if __name__ == "__main__":
    unittest.main()
