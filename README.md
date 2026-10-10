# Agent Kit

Переносимые личные инструкции и 10 собственных скиллов для разработки и учебных работ. Один репозиторий работает как marketplace для Codex и Claude Code. Скилл `setup` подключает инструкции к новому окружению; профиль с личными данными хранится отдельно и не экспортируется.

## Подключение из GitHub

После публикации замени `OWNER/REPO` на свой репозиторий. Публичный репозиторий доступен всем; для private нужна настроенная GitHub-аутентификация клиента.

Codex CLI:

```sh
codex plugin marketplace add OWNER/REPO --ref main
codex plugin add personal@agent-kit
```

В новой сессии попроси: «Прочитай и выполни скилл setup из плагина personal». Если интерфейс показывает onboarding, начни с него.

Claude Code:

```text
/plugin marketplace add OWNER/REPO
/plugin install personal@agent-kit
/personal:setup
```

Для обновления Codex выполни `codex plugin marketplace upgrade agent-kit`, затем `codex plugin add personal@agent-kit`, и проверь установленную версию через `codex plugin list`. В Claude открой `/plugin`, раздел Marketplaces, и включи обновления этого marketplace или обнови его вручную. Изменения уже скопированных локальных инструкций агент объединяет отдельно, сохраняя локальные правила и профиль.

Форматы и команды: [Codex plugins](https://developers.openai.com/plugins/build/plugins), [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Claude installation and updates](https://code.claude.com/docs/en/discover-plugins).

## Что переносится

- 10 собственных скиллов, общая университетская схема, Python-механизм допуска критика и его тесты.
- Общий стиль общения и правила локального профиля.
- Отдельные профили Big Data, виртуализации и Orchid. Orchid применяется только к соответствующему проекту.
- Настройка обоих клиентов и отдельный агент-критик для Claude.

Точный список файлов: [FILES.md](FILES.md). Границы экспорта: [docs/EXPORT.md](docs/EXPORT.md). Зависимости и ограничения: [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).

## Локальная проверка

```sh
python3 scripts/check.py
PYTHONDONTWRITEBYTECODE=1 python3 plugins/personal/skills/university-text-critic/scripts/test_critic_gate.py -v
```

Критик работает на Linux/WSL и macOS с Python 3.10+. На нативном Windows он останавливается с сообщением о недоступном `fcntl`: сначала нужно заменить файловую блокировку, сохранив защиту от одновременной записи. Это ограничение критика и зависимого допуска DOCX, а не всего плагина. Windows-ориентированный профиль Orchid сохраняет собственные требования к платформе.

## Публикация

Создай пустой GitHub-репозиторий и передай его URL агенту. Он загрузит только содержимое этой папки. Учебные работы, личная память, настройки аккаунтов и сторонние плагины в репозиторий не входят.

Сторонние плагины устанавливаются из актуальных upstream-источников без фиксации версии. Номер `1.0.0` относится только к нашему пакету и нужен клиентам для обновления кэша.
