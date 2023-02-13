import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message,Chat,Contact
from .views import get_last_10_messages
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        print(data)
        userchat = Chat.objects.get(id=data['chatId'])
        number_of_chats = data['number_of_chats']
        messages = get_last_10_messages(userchat.id)
        if messages is not None:
            content = {
                'command':'messages',
                'messages':self.messages_to_json(messages,number_of_chats)
            }
            self.send_message(content)
        else:
            self.send_message({'command': 'messages', 'messages': [ ]})
    
    def new_message(self,data):
        author = data['from']
        chat_id = data['chatId']
        author_user = get_object_or_404(User,id=author)
        contact = get_object_or_404(Contact,user=author_user)
        content = data['message']
        message = Message.objects.create(
            contact=contact,content=content
        )
        new_message = get_object_or_404(Message,id=message.id)
        print(new_message)
        res =Chat.objects.filter(id=chat_id)
        for i in res:
            i.messages.add(Message.objects.get(id=message.id))
        # Chat.participants.add(Message.objects.get(id=message.id))
        Chat.objects.filter(id=chat_id).update(updated_timestamp=timezone.now())
        content={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self,messages,number_of_chats):
        result = []
        print(messages)
        print(number_of_chats)
        for message in messages.messages.all()[:number_of_chats]:
            print(message)
            result.append(self.message_to_json(message))
        return result
    
    def message_to_json(self,message):
        return {
            'id':message.contact.user.id,
            'author':message.contact.user.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
        }
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        # message = data['message']
        self.commands[data['command']](self,data)

    def send_chat_message(self,message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self,message):
        print(message)
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        self.send(text_data=json.dumps(message))