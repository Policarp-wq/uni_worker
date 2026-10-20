"""Exercise hook decisions on synthetic commands; never execute those commands."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from document_read_guard import check, check_read


def main():
    cases = [
        ('cat report.pdf', True),
        ('cat "Задание 3.DOCX"', True),
        ('python3 -c "from docx import Document; Document(\'input.docx\')"', True),
        ('unzip presentation.pptx', True),
        ('strings old.doc', True),
        ('cat report.md', False),
        ('cat table.csv diagram.svg table.xlsx page.html book.epub old.ppt', False),
        ('python3 -c "Image.open(\'photo.png\')"', False),
        ('python3 -c "Image.new(\'RGB\', (10,10)).save(\'new.png\')"', False),
        ('python3 -c "Document().save(\'new.docx\')"', False),
        ('python3 -c "open(\'new.pdf\', \'wb\').write(b\'x\')"', False),
        ('python3 -c "Path(\'new.docx\').write_bytes(b\'x\')"', False),
        ('cat report.md > output.docx', False),
        ('cat input.pdf > output.md', True),
        ('python3 -c "Document(\'input.docx\').save(\'output.docx\')"', True),
        ('markitdown input.pdf -o input.md', False),
        ('markitdown input.pdf -o input.md; cat secret.docx', True),
        ('rg --files -g "*.pdf"', False),
        ('rg --files -g "*.mp3"', False),
        ('rg --files; cat secret.pdf', True),
        ('rg --files; markitdown speech.mp3 -o speech.md', True),
        ('rg --files < speech.mp3', True),
        ('rg --files "$(cat speech.mp3)"', True),
        ('ffmpeg -i speech.wav converted.flac', True),
        ('cat speech.mp3', True),
        ('markitdown speech.m4a -o speech.md', True),
        ('python3 -c "open(\'SPEECH.OPUS\', \'rb\')"', True),
        ('markitdown speech.mp3 -o speech.md; cat report.md', True),
        ('cat report.md\ncat input.pdf', True),
        ('PY=python3; $PY inspect.py report.docx', True),
        ('$PY inspect.py report.md', False),
        ('.venv/bin/python -I -c "Document(\'a.docx\')"', True),
    ]
    with tempfile.TemporaryDirectory() as temp:
        for command, blocked in cases:
            assert bool(check(command, temp)) == blocked, command
        Path(temp, 'Задание 3.md').write_text('Готовая текстовая копия', encoding='utf-8')
        assert 'Markdown already exists' in check('markitdown "Задание 3.docx" -o another.md', temp)
        assert check('cat "Задание 3.docx"', temp)
        assert check('cat "Задание 3.md"', temp) is None
        Path(temp, 'empty.md').write_text(' \n', encoding='utf-8')
        assert check('markitdown empty.pdf -o empty.md', temp) is None
        Path(temp, 'invalid.md').write_bytes(b'\xff')
        assert check('markitdown invalid.pdf -o invalid.md', temp) is None
        work = Path(temp, 'PR6')
        work.mkdir()
        Path(work, 'PR6.md').write_text('Одобренный отчёт', encoding='utf-8')
        Path(work, 'PR6.docx').write_bytes(b'x')
        assert check('ls -la PR6.docx; python3 build.py', str(work))
        Path(work, '.critic-approve').write_text(json.dumps(
            {'source': str(Path(work, 'PR6.md').resolve())}), encoding='utf-8')
        assert check('ls -la PR6.docx; python3 build.py', str(work)) is None
        assert check('markitdown PR6.docx -o /tmp/check.md | tail -3', str(work)) is None
        assert check('python3 -c "Document(\'PR6.docx\')"', str(work)) is None
        assert check('python3 -c "Document(\'PR6.docx\'); Document(\'task.docx\')"', str(work))
        assert check('cat task.docx', str(work))
        Path(work, 'other.md').write_text('Другой текст', encoding='utf-8')
        assert check('cat other.docx', str(work))
        hook = Path(__file__).with_name('document_read_guard.py')
        for key in ('command', 'cmd'):
            result = subprocess.run([sys.executable, str(hook)], input=json.dumps({
                'cwd': temp, 'tool_input': {key: 'markitdown "Задание 3.docx" -o output.md'}
            }), text=True, capture_output=True, check=True)
            decision = json.loads(result.stdout)['hookSpecificOutput']
            assert decision['permissionDecision'] == 'deny'
            assert 'Markdown already exists' in decision['permissionDecisionReason']
        assert check_read('report.docx', temp)
        assert check_read('REPORT.PDF', temp)
        assert check_read('slides.pptx', temp)
        assert check_read('speech.mp3', temp)
        assert check_read('report.md', temp) is None
        assert check_read('photo.png', temp) is None
        assert check_read('table.xlsx', temp) is None
        assert str(Path(temp, 'Задание 3.md')) in check_read('Задание 3.docx', temp)
        for path in ('input.docx', 'speech.wav'):
            result = subprocess.run([sys.executable, str(hook)], input=json.dumps({
                'cwd': temp, 'tool_name': 'Read', 'tool_input': {'file_path': path}
            }), text=True, capture_output=True, check=True)
            assert json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'] == 'deny'
        result = subprocess.run([sys.executable, str(hook)], input=json.dumps({
            'cwd': temp, 'tool_name': 'Read', 'tool_input': {'file_path': 'notes.md'}
        }), text=True, capture_output=True, check=True)
        assert result.stdout == ''
    print(f'PASS: {len(cases)} command cases, cached/empty/invalid Markdown, approved deliverables, both event keys')


if __name__ == '__main__':
    main()
