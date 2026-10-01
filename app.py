import html
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fayrouz-store-secret-key-2026'

# ==========================================
# 1. بيانات المتجر والمنتجات
# ==========================================
STORE_INFO = {
    "name": "فيروز",
    "whatsapp_number": "96890195140",
    "display_phone": "+968 9019 5140"
}

PRODUCTS = [
    {
        "id": 1,
                "name": "مباخر خشب طبيعي",
        "price": 25.00,
        "category": "مباخر",
        "featured": True,
        "image": "https://i.supaimg.com/9a716999-3550-4c68-bdba-52ed7a67a8e2/d73a73ae-6bb4-4f2b-a3f4-bcc352b5ce03.jpg",
        "description": "شغل يدوي خشب الورد الطبيعي"
    },
    {
        "id": 2,
        "name": "بوكس اوفال مطعم صدف طبيعي حجم 30×20",
        "price": 45.00,
        "category": "بوكس موزاييك مع ريزن ",
        "featured": True,
        "image": "https://i.supaimg.com/9a716999-3550-4c68-bdba-52ed7a67a8e2/13d3fa30-a8cf-45da-8805-f10ab70198af.jpg",
        "description": "حجم 18*13."
    },
    {
        "id": 3,
    "name": "بوكس موزاييك سادة وشعار السلطنة",
        "price": 18.00,
        "category": "",
        "featured": False,
        "image": "https://i.supaimg.com/9a716999-3550-4c68-bdba-52ed7a67a8e2/7ac23546-8eef-4186-a38d-054ff754d17d.jpg",
        "description": " خشب ورد طبيعي وشعار السلطنة UV400."
    },
    {
        "id": 4,
        "name": "مباخر خشب طبيعي",

        "price": 60.00,
        "category": "حقائب",
        "featured": True,
        "image": "https://i.supaimg.com/9a716999-3550-4c68-bdba-52ed7a67a8e2/45a0227f-3ea9-4f59-a484-055dca067e8a.jpg",
        "description": "مصنوعة من الجلد الطبيعي الممتاز."
    }
]

# ==========================================
# 2. وظائف الأمان والحماية من الثغرات (XSS Sanitization)
# ==========================================
def sanitize_text(text):
    if not text:
        return ""
    return html.escape(str(text).strip())

# ==========================================
# 3. واجهة المستخدم (HTML + Tailwind CSS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ store.name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
        body { font-family: 'Cairo', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 pb-24">

    <!-- Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-md">
                    <i class="fas fa-gem"></i>
                </div>
                <div>
                    <h1 class="font-bold text-slate-900 leading-tight text-lg">{{ store.name }}</h1>
                    <p class="text-xs text-slate-500">متجر إلكتروني معتمد</p>
                </div>
            </div>
            <button onclick="openCart()" class="relative p-2 text-slate-700 hover:text-emerald-600 transition">
                <i class="fas fa-shopping-bag text-2xl"></i>
                <span id="cart-count" class="absolute -top-1 -right-1 bg-rose-500 text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center hidden">0</span>
            </button>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="max-w-md mx-auto bg-white border-b border-slate-200 flex text-center font-semibold text-sm">
        <button id="tab-featured" onclick="switchTab('featured')" class="flex-1 py-3 border-b-2 border-emerald-600 text-emerald-600 transition font-bold">
            🌟 المنتجات المميزة
        </button>
        <button id="tab-all" onclick="switchTab('all')" class="flex-1 py-3 border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition">
            🛍️ جميع المنتجات
        </button>
    </nav>

    <!-- Main Content -->
    <main class="max-w-md mx-auto px-4 pt-4">

        <!-- Section 1: Featured -->
        <section id="sec-featured">
            <div class="mb-3">
                <h2 class="font-bold text-slate-800 text-lg">المنتجات الأكثر طلباً 🔥</h2>
            </div>
            <div class="grid grid-cols-2 gap-3">
                {% for item in featured %}
                <div class="bg-white rounded-2xl p-2.5 shadow-sm border border-slate-100 flex flex-col justify-between">
                    <div>
                        <img src="{{ item.image }}" class="w-full h-32 object-cover rounded-xl mb-2" alt="{{ item.name }}">
                        <h3 class="font-bold text-sm text-slate-800 line-clamp-1">{{ item.name }}</h3>
                        <p class="text-xs text-slate-500 mb-2 line-clamp-1">{{ item.description }}</p>
                    </div>
                    <div class="flex items-center justify-between mt-1 pt-2 border-t border-slate-50">
                        <span class="font-bold text-emerald-600 text-sm">${{ "%.2f"|format(item.price) }}</span>
                        <button onclick="addToCart({{ item.id }}, '{{ item.name }}', {{ item.price }})" class="bg-emerald-600 text-white w-8 h-8 rounded-lg flex items-center justify-center hover:bg-emerald-700 transition">
                            <i class="fas fa-plus text-xs"></i>
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Section 2: All Products & Search -->
        <section id="sec-all" class="hidden">
            <div class="mb-4">
                <div class="relative">
                    <input type="text" id="search-input" oninput="filterProducts()" placeholder="ابحث عن منتج..." class="w-full bg-white border border-slate-200 rounded-xl py-2.5 pr-10 pl-4 text-sm focus:outline-none focus:border-emerald-500 shadow-sm">
                    <i class="fas fa-search absolute right-3.5 top-3.5 text-slate-400 text-sm"></i>
                </div>
            </div>

            <div id="all-products-grid" class="grid grid-cols-2 gap-3">
                {% for item in all_products %}
                <div class="product-card bg-white rounded-2xl p-2.5 shadow-sm border border-slate-100 flex flex-col justify-between" data-name="{{ item.name }}">
                    <div>
                        <img src="{{ item.image }}" class="w-full h-32 object-cover rounded-xl mb-2" alt="{{ item.name }}">
                        <h3 class="font-bold text-sm text-slate-800 line-clamp-1">{{ item.name }}</h3>
                        <p class="text-xs text-slate-500 mb-2 line-clamp-1">{{ item.description }}</p>
                    </div>
                    <div class="flex items-center justify-between mt-1 pt-2 border-t border-slate-50">
                        <span class="font-bold text-emerald-600 text-sm">${{ "%.2f"|format(item.price) }}</span>
                        <button onclick="addToCart({{ item.id }}, '{{ item.name }}', {{ item.price }})" class="bg-emerald-600 text-white w-8 h-8 rounded-lg flex items-center justify-center hover:bg-emerald-700 transition">
                            <i class="fas fa-plus text-xs"></i>
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
    </main>

    <!-- Cart Modal -->
    <div id="cart-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden flex justify-end">
        <div class="bg-white w-full max-w-md h-full flex flex-col justify-between p-4 overflow-y-auto">
            <div>
                <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                    <h2 class="font-bold text-lg text-slate-800">سلة التسوق 🛒</h2>
                    <button onclick="closeCart()" class="text-slate-400 hover:text-slate-600 text-xl"><i class="fas fa-times"></i></button>
                </div>

                <div id="cart-items-container" class="py-4 space-y-3"></div>
            </div>

            <div id="cart-footer" class="border-t border-slate-100 pt-4 space-y-3 hidden">
                <div class="flex justify-between items-center text-base font-bold">
                    <span>المجموع الإجمالي:</span>
                    <span id="cart-total-price" class="text-emerald-600">$0.00</span>
                </div>
                <button onclick="showCheckoutForm()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition shadow-md">
                    متابعة وتحديد مكان التوصيل 🚚
                </button>
            </div>
        </div>
    </div>

    <!-- Checkout Modal -->
    <div id="checkout-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-md rounded-2xl p-5 shadow-xl space-y-4">
            <div class="flex justify-between items-center pb-2 border-b border-slate-100">
                <h3 class="font-bold text-slate-800">مكان التوصيل والبيانات</h3>
                <button onclick="closeCheckout()" class="text-slate-400 hover:text-slate-600"><i class="fas fa-times"></i></button>
            </div>

            <form id="checkout-form" onsubmit="submitOrder(event)" class="space-y-3">
                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">الاسم الكامل *</label>
                    <input type="text" id="cust-name" required class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">رقم الهاتف *</label>
                    <input type="tel" id="cust-phone" required placeholder="9XXXXXXX" class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">المدينة / المنطقة *</label>
                    <input type="text" id="cust-city" required class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">مكان التوصيل والعنوان بالتفصيل *</label>
                    <textarea id="cust-address" required rows="2" placeholder="المنطقة، الشارع، أو أي علامة مميزة" class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-emerald-500"></textarea>
                </div>

                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition shadow-md">
                    إكمال وتأكيد الطلب
                </button>
            </form>
        </div>
    </div>

    <!-- Contact Info Modal (Show Number Directly) -->
    <div id="contact-modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-md rounded-2xl p-6 shadow-2xl text-center space-y-4">
            <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-3xl">
                <i class="fas fa-check-circle"></i>
            </div>
            
            <h3 class="font-bold text-xl text-slate-800">تم تجهيز طلبك بنجاح!</h3>
            <p class="text-sm text-slate-600">لتأكيد الطلب واستكماله، يرجى التواصل معنا المباشر على الرقم التالي:</p>
            
            <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4 my-2">
                <p class="text-xs text-slate-400 mb-1">رقم التواصل المباشر للمتجر</p>
                <a href="tel:{{ store.whatsapp_number }}" class="text-2xl font-black text-emerald-600 tracking-wider dir-ltr block hover:underline">
                    {{ store.display_phone }}
                </a>
            </div>

            <div class="flex flex-col gap-2 pt-2">
                <a href="https://wa.me/{{ store.whatsapp_number }}" target="_blank" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition flex items-center justify-center gap-2">
                    <i class="fab fa-whatsapp text-lg"></i> تواصل معنا عبر الواتساب
                </a>
                <a href="tel:{{ store.whatsapp_number }}" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold py-3 rounded-xl transition flex items-center justify-center gap-2">
                    <i class="fas fa-phone-alt"></i> الاتصال المباشر
                </a>
            </div>
        </div>
    </div>

    <script>
        let cart = [];

        function switchTab(tab) {
            document.getElementById('sec-featured').classList.toggle('hidden', tab !== 'featured');
            document.getElementById('sec-all').classList.toggle('hidden', tab !== 'all');
            
            document.getElementById('tab-featured').className = tab === 'featured' 
                ? "flex-1 py-3 border-b-2 border-emerald-600 text-emerald-600 transition font-bold" 
                : "flex-1 py-3 border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition";
            
            document.getElementById('tab-all').className = tab === 'all' 
                ? "flex-1 py-3 border-b-2 border-emerald-600 text-emerald-600 transition font-bold" 
                : "flex-1 py-3 border-b-2 border-transparent text-slate-500 hover:text-slate-800 transition";
        }

        function filterProducts() {
            const q = document.getElementById('search-input').value.toLowerCase();
            document.querySelectorAll('.product-card').forEach(card => {
                const name = card.getAttribute('data-name').toLowerCase();
                card.style.display = name.includes(q) ? 'flex' : 'none';
            });
        }

        function addToCart(id, name, price) {
            const existing = cart.find(item => item.id === id);
            if (existing) {
                existing.quantity += 1;
            } else {
                cart.push({ id, name, price, quantity: 1 });
            }
            updateCartUI();
        }

        function updateCartUI() {
            const countElem = document.getElementById('cart-count');
            const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
            
            if (totalQty > 0) {
                countElem.innerText = totalQty;
                countElem.classList.remove('hidden');
            } else {
                countElem.classList.add('hidden');
            }

            const container = document.getElementById('cart-items-container');
            if (cart.length === 0) {
                container.innerHTML = '<p class="text-center text-slate-400 py-8">السلة فارغة حالياً</p>';
                document.getElementById('cart-footer').classList.add('hidden');
                return;
            }

            let total = 0;
            container.innerHTML = cart.map(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                return `
                    <div class="flex items-center justify-between bg-slate-50 p-3 rounded-xl">
                        <div>
                            <h4 class="font-bold text-sm text-slate-800">${item.name}</h4>
                            <p class="text-xs text-emerald-600 font-semibold">$${item.price.toFixed(2)}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <button onclick="changeQty(${item.id}, -1)" class="w-6 h-6 bg-slate-200 rounded text-xs font-bold">-</button>
                            <span class="text-sm font-bold">${item.quantity}</span>
                            <button onclick="changeQty(${item.id}, 1)" class="w-6 h-6 bg-slate-200 rounded text-xs font-bold">+</button>
                        </div>
                    </div>
                `;
            }).join('');

            document.getElementById('cart-total-price').innerText = `$${total.toFixed(2)}`;
            document.getElementById('cart-footer').classList.remove('hidden');
        }

        function changeQty(id, delta) {
            const item = cart.find(i => i.id === id);
            if (item) {
                item.quantity += delta;
                if (item.quantity <= 0) {
                    cart = cart.filter(i => i.id !== id);
                }
            }
            updateCartUI();
        }

        function openCart() { document.getElementById('cart-modal').classList.remove('hidden'); }
        function closeCart() { document.getElementById('cart-modal').classList.add('hidden'); }
        function showCheckoutForm() { closeCart(); document.getElementById('checkout-modal').classList.remove('hidden'); }
        function closeCheckout() { document.getElementById('checkout-modal').classList.add('hidden'); }

        async function submitOrder(e) {
            e.preventDefault();
            
            const payload = {
                name: document.getElementById('cust-name').value,
                phone: document.getElementById('cust-phone').value,
                city: document.getElementById('cust-city').value,
                address: document.getElementById('cust-address').value,
                cart: cart
            };

            try {
                const response = await fetch('/checkout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const res = await response.json();
                if (res.success) {
                    closeCheckout();
                    document.getElementById('contact-modal').classList.remove('hidden');
                } else {
                    alert(res.message || 'حدث خطأ في تقديم الطلب.');
                }
            } catch (err) {
                alert('عذراً، تعذر الاتصال بالسيرفر.');
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# 4. مسارات بايثون (Flask Routes)
# ==========================================

@app.route('/')
def home():
    featured_products = [p for p in PRODUCTS if p.get('featured')]
    return render_template_string(HTML_TEMPLATE, store=STORE_INFO, featured=featured_products, all_products=PRODUCTS)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json or {}
    
    # حماية وتطهير المدخلات لمنع ثغرات XSS
    client_name = sanitize_text(data.get('name'))
    client_phone = sanitize_text(data.get('phone'))
    client_address = sanitize_text(data.get('address'))
    cart_items = data.get('cart', [])

    if not client_name or not client_phone or not client_address or not cart_items:
        return jsonify({'success': False, 'message': 'يرجى إكمال جميع الحقول وإضافة منتج للسلة.'}), 400

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
