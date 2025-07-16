def reward_message_processor(request):
    message = request.session.pop('reward_message', None)
    emojis = request.session.pop('reward_emojis', None)
    return {
        'reward_message': message,
        'reward_emojis': emojis,
    }
