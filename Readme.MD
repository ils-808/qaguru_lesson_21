# qa_guru_python_8_22
Задание к двадцать второму уроку курса QA Guru

## Локальный запуск на эмулированном устройсте
pytest -s -v context=local .

## Удаленный запуск на BrowserStack
pytest -s -v --context=remote .

## Просмотр отчета allure
allure serve .\allure-results\