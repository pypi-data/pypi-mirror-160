# kroki-python

Lib for interaction with https://kroki.io

## Запустить тест:

```sh
poetry run poe docs
```

Или запусить task в vs code - F1 -> Task: Run task -> docs

## Загрузить пакет в pypi

Собрать и опубликовать пакет

```sh
poetry build && poetry publish
```

Логин: konstantin-dudersky

## Задача poe

Дописать в файл pyproject.toml:

```toml
docs = {script = "konstantin_docs.main:generate_images(path_src='test/dia_src', path_dist='test/dia_dist')"}
```

## Создать задачу vscode

В файле .vscode/tasks.json:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "docs",
      "type": "shell",
      "command": "poetry run poe docs"
    }
  ]
}
```
