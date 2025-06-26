from django import template

register = template.Library()

@register.filter
def neuro_gradient(color):
    gradients = {
        'green': 'bg-gradient-to-b from-emerald-300 via-green-500 to-emerald-900',      # flow state
        'blue': 'bg-gradient-to-b from-sky-300 via-blue-500 to-indigo-900',              # clarity / deep work
        'yellow': 'bg-gradient-to-b from-yellow-200 via-amber-400 to-yellow-900',        # sparks / ideation
        'purple': 'bg-gradient-to-b from-fuchsia-500 via-purple-600 to-violet-900',      # focus / zone in
        'pink': 'bg-gradient-to-b from-pink-500 via-rose-500 to-pink-600',               # joy / creativity
        'red': 'bg-gradient-to-b from-red-400 via-red-600 to-red-900',                   # grind / frustration
    }
    return gradients.get(color, 'bg-gradient-to-b from-gray-500 via-gray-700 to-gray-900')
