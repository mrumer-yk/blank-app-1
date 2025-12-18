

import streamlit as st
import time
import random

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="ShopStream", layout="wide", page_icon="🛍️")

# --------------------------------------------------
# SCOPED CSS (ONLY PRODUCT IMAGES)
# --------------------------------------------------
st.markdown("""
<style>
.product-img img {
    width: 100%;
    height: 300px;
    object-fit: cover;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

AGENT_DISCOUNT_MULTIPLIER = 0.8  # 20% off

# --------------------------------------------------
# PRODUCT DATA
# --------------------------------------------------
PRODUCTS = [
    {
        "id": 1,
        "name": "Royal Banarasi Silk Saree",
        "description": "Traditional red Banarasi silk saree with intricate gold zari work.",
        "price": 4999,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 2,
        "name": "Handcrafted Ceramic Mug",
        "description": "Artisanal ceramic coffee mug, perfect for your morning brew.",
        "price": 499,
        "category": "Home & Kitchen",
        "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 3,
        "name": "Luxury Matte Lipstick Set",
        "description": "Long-lasting matte finish lipsticks in 5 vibrant shades.",
        "price": 1299,
        "category": "Makeup",
        "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 4,
        "name": "Vintage Glass Storage Jars",
        "description": "Set of 3 airtight glass jars for kitchen storage.",
        "price": 899,
        "category": "Home & Kitchen",
        "image": "https://images.unsplash.com/photo-1584473457406-6240486418e9?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 5,
        "name": "Elegant Cotton Saree",
        "description": "Lightweight cotton saree with modern floral prints.",
        "price": 1499,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1583391733958-e026609b5558?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 6,
        "name": "Minimalist Mason Jars",
        "description": "Pack of 6 versatile mason jars for smoothies or spices.",
        "price": 650,
        "category": "Home & Kitchen",
        "image": "https://images.unsplash.com/photo-1605307374665-27a36c53e8fb?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 7,
        "name": "Premium Eyeshadow Palette",
        "description": "Highly pigmented eyeshadows with shimmer and matte textures.",
        "price": 1850,
        "category": "Makeup",
        "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
    },
    {
        "id": 8,
        "name": "Designer Tea Cup Set",
        "description": "Fine bone china tea cups with matching saucers.",
        "price": 2100,
        "category": "Home & Kitchen",
        "image": "https://images.unsplash.com/photo-1577937927133-66ef06acdf18?q=80&w=800&auto=format&fit=crop",
    },
]

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
st.session_state.setdefault("cart", {})
st.session_state.setdefault("is_agent", False)
st.session_state.setdefault("show_modal", False)

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------
def add_to_cart(pid):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("Item added to cart 🛒")

def activate_agent():
    with st.spinner("Generating Agent Code..."):
        time.sleep(1.5)

    st.session_state.is_agent = True
    st.session_state.show_modal = False
    st.success(f"Agent Activated: AGENT-{random.randint(1000,9999)}")
    st.balloons()

# --------------------------------------------------
# SIDEBAR CART
# --------------------------------------------------
with st.sidebar:
    st.header("🛒 Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for pid, qty in st.session_state.cart.items():
            prod = next(p for p in PRODUCTS if p["id"] == pid)
            price = prod["price"]
            if st.session_state.is_agent:
                price *= AGENT_DISCOUNT_MULTIPLIER
            total += price * qty
            st.write(f"**{prod['name']}**")
            st.caption(f"Qty: {qty} | ₹{price:.2f}")

        st.divider()
        if st.session_state.is_agent:
            st.success("Agent Discount Applied (20%)")
        st.subheader(f"Total: ₹{total:.2f}")
        st.button("Proceed to Checkout", type="primary", use_container_width=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🛍️ ShopStream")
with c2:
    if not st.session_state.is_agent:
        st.button("Become an Agent 🛡️", on_click=lambda: st.session_state.update(show_modal=True))
    else:
        st.button("✅ Agent Active", disabled=True)

st.divider()
st.info("### Exclusive Lifestyle Collection\nDiscover premium ethnic wear, home decor & beauty products.")

# --------------------------------------------------
# AGENT MODAL
# --------------------------------------------------
if st.session_state.show_modal:
    with st.expander("🔐 Agent Registration", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("Generate & Activate", on_click=activate_agent)
        with col_b:
            st.button("Cancel", on_click=lambda: st.session_state.update(show_modal=False))

# --------------------------------------------------
# PRODUCT GRID (STABLE IMAGES)
# --------------------------------------------------
cols = st.columns(2)

for i, product in enumerate(PRODUCTS):
    with cols[i % 2]:
        with st.container(border=True):

            # FIXED IMAGE (HTML)
            st.markdown(
                f"""
                <div class="product-img">
                    <img src="{product['image']}">
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(product["category"])
            st.subheader(product["name"], anchor=False)
            st.write(product["description"])

            price = product["price"]
            if st.session_state.is_agent:
                d = price * AGENT_DISCOUNT_MULTIPLIER
                st.markdown(
                    f"### ~~₹{price}~~ <span style='color:green'>₹{d:.2f}</span>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(f"### ₹{price}")

            st.button(
                "Add to Cart",
                key=f"add_{product['id']}",
                use_container_width=True,
                on_click=add_to_cart,
                args=(product["id"],)
            )
