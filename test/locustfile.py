import socketio
from locust import User, task, between, events


class SocketIOUser(User):
    wait_time = between(1, 2)

    def on_start(self):
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/'])

    def on_stop(self):
        self.client.disconnect()

    @task
    def send_message(self):
        self.client.emit('send_notification', {'msg': 'Hello, World!'}, namespace='/')
        # Manually firing a success event
        self.environment.events.request.fire(
            request_type='WebSocket',
            name='send_notification',
            response_time=1000,
            response_length=0,
            exception=None,
            context={},
            user=self
        )

    @task
    def receive_message(self):
        @self.client.on('receive_notification', namespace='/')
        def on_message(data):
            print('Received message:', data)
            # Record a received message as a success
            self.environment.events.request.fire(
                request_type='WebSocket Recv',
                name='receive_notification',
                response_time=1000,
                response_length=len(str(data)),
                exception=None,
                context={},
                user=self
            )
