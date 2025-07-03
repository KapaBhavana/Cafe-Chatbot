import re

def handle_chat_message(message, session, menu_items):
    lang = session.get('lang', 'en')
    if message.lower() in ['english', 'hindi', 'telugu', 'tamil']:
        lang_map = {'english': 'en', 'hindi': 'hi', 'telugu': 'te', 'tamil': 'ta'}
        session['lang'] = lang_map[message.lower()]
        return f"✅ Language set to {message.title()}. How can I assist you?"

    if re.search(r'order|menu|want|get|buy', message, re.IGNORECASE):
        return get_menu(menu_items, lang)

    for item in menu_items:
        item_name = item['name'].get(lang, item['name']['en']).lower()
        if item_name in message.lower():
            session['cart'].append(item)
            return f"🛒 {item['name'][lang]} added to your cart."

    if "summary" in message.lower():
        return get_order_summary(session['cart'], lang)

    if "cancel" in message.lower():
        session['cart'] = []
        return "❌ Your order has been canceled."

    if "pay" in message.lower():
        if not session['cart']:
            return "🛒 Your cart is empty."
        total = sum(i['price'] for i in session['cart'])
        session['cart'] = []
        return f"💳 Payment processed successfully! Total paid: ₹{total}"

    return "🤖 Say 'menu' to see items, or try ordering something!"

def get_menu(menu_items, lang):
    menu_text = "📋 Menu:\n"
    for item in menu_items:
        name = item['name'][lang]
        price = item['price']
        image = item.get('image', '')
        menu_text += f"{name} - ₹{price}\n"
        if image:
            menu_text += f"<img src='{image}' width='100'><br>\n"
    return menu_text

def get_order_summary(cart, lang):
    if not cart:
        return "🛒 Your cart is empty."
    summary = "🧾 Order Summary:\n"
    total = 0
    for item in cart:
        name = item['name'][lang]
        price = item['price']
        total += price
        summary += f"- {name} - ₹{price}\n"
    summary += f"\nTotal: ₹{total}"
    return summary
