## Изменения

- ReceiveThread: добавлен сигнал connection_lost, вызов recv() обернут в try/except
- SendThread: добавлен метод stop(), вызов send() обёрнут в try/except
- MainWindow: добавлены on_connection_lost() и closeEvent()

## Потеря соединения

В ReceiveThread.run() вызов self.net.recv() находится в try/except (OSError, ValueError). Если recv() вернул None (сервер закрыл соединение), цикл тоже завершается. После выхода из цикла поток отправляет сигнал connection_lost. В MainWindow он подключён к on_connection_lost(): в чат выводится сообщение "Соединение с сервером потеряно", поле ввода и кнопка Send блокируются

## Остановка SendThread

Метод stop() кладет в очередь None, run() при получении None выходит из цикла. В closeEvent() вызываются send_thread.stop() и send_thread.wait()

## Проверки

- сервер и два клиента: сообщения доставляются
- остановка сервера при открытом клиенте: появляется сообщение о потере соединения, ошибок в терминале нет
- закрытие окна клиента: программа завершается
