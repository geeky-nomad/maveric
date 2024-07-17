const sampleDataset = {
  "/welcome": {
    "message": "Welcome to Hiketron chatbot, How can I assist you today?",
    "type": "select-category",
    "options": [
      {
        "text": "Show me Liquid soap dispensers",
        "value": "Liquid Soap Dispensers"
      },
      {
        "text": "Show me Laundry Detergent",
        "value": "Laundry Detergent"
      },
      {
        "text": "Show me Skin Care",
        "value": "Skin Care"
      },
      {
        "text": "Show me Hair Care",
        "value": "Hair Care"
      },
      {
        "text": "Explore our Gift Card section",
        "value": "Gift Card"
      }
    ]
  },
  "/select-category": {
    "message": "What kind of hair care are you looking for?",
    "type": "select-sub-category",
    "options": [
      {
        "text": "Voguish Man Shampoo Conditioner Set 8 Oz Tube",
        "value": "voguish-man-shampoo-conditioner-set-8-oz-tube"
      },
      {
        "text": "Keratinpro Conditioner",
        "value": "keratinpro-conditioner"
      },
      {
        "text": "Keratinpro Shampoo 8 Oz Tube",
        "value": "keratinpro-shampoo-8-oz-tube"
      },
      {
        "text": "Experimint Conditioner 8 Oz Tube",
        "value": "experimint-conditioner-8-oz-tube"
      },
      {
        "text": "Experimint Shampoo 8 Oz Tube",
        "value": "experimint-shampoo-8-oz-tube"
      },
      {
        "text": "Rejuvenating Shampoo",
        "value": "rejuvenating-shampoo"
      },
      {
        "text": "Rejuvenating Conditioner 8 Oz Tube",
        "value": "rejuvenating-conditioner-8-oz-tube"
      },
      {
        "text": "Voguish Man Conditioner 8 Oz Tube",
        "value": "voguish-man-conditioner-8-oz-tube"
      },
      {
        "text": "Voguish Man Shampoo 8 Oz Tube",
        "value": "voguish-man-shampoo-8-oz-tube"
      }
    ]
  },
  "/select-sub-category": {
    "message": "Here is the matching product.",
    "type": "checkout",
    "options": [
      {
        "title": "experimint-shampoo-8-oz-tube",
        "variant_price": 26.99,
        "image_src": "https://cdn.shopify.com/s/files/1/2672/1228/products/ExperiMintShampoo_160509064.jpg?v=1602790580",
        "product_url": "https://www.hiketron.com/products/experimint-shampoo-8-oz-tube"
      },
      {
        "title": "experimint-shampoo-8-oz-tube",
        "variant_price": 26.99,
        "image_src": "https://cdn.shopify.com/s/files/1/2672/1228/products/ExperiMintShampoo_160509064.jpg?v=1602790580",
        "product_url": "https://www.hiketron.com/products/experimint-shampoo-8-oz-tube"
      }
    ]
  },
  "/query": {
    "message": "Here are the matching products.",
    "type": "select-sub-category",
    "options": [
      {
        "text": "keratinpro conditioner",
        "value": "keratinpro-conditioner"
      },
      {
        "text": "rejuvenating conditioner 8 oz tube",
        "value": "rejuvenating-conditioner-8-oz-tube"
      },
      {
        "text": "experimint conditioner 8 oz tube",
        "value": "experimint-conditioner-8-oz-tube"
      }
    ]
  }
};