"""
Generate content for the features that svelte-commerce supports by
using ChatGPT.
"""

from typing import List, Dict
from os import path
from time import sleep
from re import sub

from requests import post

# Define some global variables
OPENAI_KEY = ""


class TooManyRequestsException(Exception):
    "Raised when OpenAI returns a 429 error"
    pass

def get_features() -> List[str]:
    """
    Return the features list
    """

    features: List[Dict] =  [
        {
            "h": 'Technology',
            "data": [
                'Composable, API-first, headless commerce solution',
                'Highly scalable enterprise level ecommerce platform  to handle high traffic',
                'Typescript for strong code base',
                'Modular code for ease of customizations',
                'Separate codebase for API, Admin and Storefront',
                'Latest GraphQL API',
                'MongoDB Database',
                'Redis Database for cache',
                'Cutting edge tech stack for better performance and better user experience',
                'Fast and Easy to use ecommerce storefront',
                'Endless customizations opportunity and IOT, AI capable',
                'Server rendered for better search engine indexing',
                'Multi vendor ecommerce',
                'Android APP',
                'iOS APP',
                'SSL Certificate Integration'
            ]
        },
        {
            "h": 'Marketing, Promotions, and Conversion Tools',
            "data": [
                'Open graph data compatibility for social media optimization',
                'Social Media Product Sharing option',
                'Email support',
                'Abandoned cart',
                'Display a recently viewed products module',
                'Add a popular search terms cloud'
            ]
        },
        {
            "h": 'Search Engine Optimization',
            "data": [
                'Auto generation of Google structured data',
                'Auto sitemap generation on daily basis',
                'Create metadata for products, categories, and content pages'
            ]
        },
        {
            "h": 'Site Management',
            "data": [
                'Custom build and SEO Optimized theme.',
                'Product Import Export',
                'Responsive design',
                'Static page management',
                'Blog engine',
                'Admin panel for store management',
                'Receive notification when inventory needs to be replenished',
                'Multi Level Categories',
                '1 SMS gateway integration',
                '1 Email gateway integration'
            ]
        },
        {
            "h": 'Catalog Management',
            "data": [
                'Automatically resize images',
                'Add breadcrumbs',
                'Product Brands',
                'Define unlimited product attributes'
            ]
        },
        {
            "h": 'Catalog Browsing',
            "data": [
                'Fast search using elasticsearch',
                'Filter products in categories and search results by price range, brands, color swatches, and other attributes with layered/faceted navigation',
                'Cart sync across devices',
                'Recommended products',
                'Deals',
                'Category landing pages',
                'Show recently viewed products',
                'Showcase new items with dynamic new product lists ',
                'Product tags (Like New, Fast selling)',
                'Include downloadable/digital products',
                'Vendor page with products list'
            ]
        },
        {
            "h": 'Product Browsing',
            "data": [
                'Muti category for products',
                'Wishlist',
                'Ratings & Reviews',
                'Multiple images and videos against single product',
                'Product Options',
                'Product Grouping',
                'Product Attributes',
                'Product Key features',
                'Zoom-in on product images ',
                'Include swatches to show colors, fabrics, and more',
                'Display stock availability',
                'Show product option selection ',
                'Include option to add product to wish list',
                'Include grouped products view'
            ]
        },
        {
            "h": 'Checkout, Payment and Shipping',
            "data": [
                '1 Payment gateway integration',
                'Save shopping cart  ',
                'Accept bank transfers',
                'Receive real-time shipping rates from UPS, UPS XML (account rates), FedEx (account rates), USPS, and DHL',
                'Provide free shipping',
                'Provide on-site order tracking from customer accounts'
            ]
        },
        {
            "h": 'Order Management',
            "data": [
                'Shipping Integration (Shippo / Shiprocket / Pickrr)',
                'View, edit, create, and fulfill orders and/or invoices from the admin panel',
                'Print invoices, packing slips, and shipping labels ',
                'Receive email notifications with order status',
                'Enable customer service representatives to create orders and customer accounts'
            ]
        },
        {
            "h": 'Customer Accounts',
            "data": [
                'Multiple user roles',
                'SMS/Email based authentication',
                'Order history',
                'View comprehensive account dashboard',
                'Include address book with unlimited addresses',
                'See order status and history',
                'Allow re-ordering from account',
                'View recently ordered items ',
                'View product reviews submitted ',
                'See order history with status updates',
                'View order tracking from account'
            ]
        },
        {
            "h": 'Customer Service',
            "data": ['Use Contact Us form', 'Live chatbot integration', 'Customizable Email Templates']
        },
        {
            "h": 'Analytics and Reporting',
            "data": ['Google Analytics integration', 'Access the reports through the admin dashboard']
        }
    ]

    data_to_return = []

    for top_level_feature in features:
        data_each = top_level_feature.get("data", [])
        data_to_return.extend(data_each)

    return data_to_return


def fetch_content_for_feature(feature: str, openai_key: str) -> str:
    """
    Fetch the content for the feature passed by using ChatGPT.
    """
    if feature == "":
        return ""

    openai_body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You're a helpful assistant"
            },
            {
                "role": "user",
                "content": "Litekart is an e-commerce platform that solves the gap between Shopify and WooCommerce"
            },
            {
                "role": "user",
                "content": f'Based on the above context, generate some content about "{feature}" as a feature of litekart. Return only the content in markdown format.'
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }

    openai_url = "https://api.openai.com/v1/chat/completions"
    openai_response = post(openai_url, headers=headers, json=openai_body)

    if not openai_response.ok:
        print("Got non OK response code from OpenAI: ",
              openai_response.status_code)
        raise TooManyRequestsException

    response_json = openai_response.json()
    choices = response_json.get("choices", [])

    if not len(choices):
        return ""

    # Parse the content now
    content: str = choices[0].get("message", {}).get("content", "")

    return content


def get_filename(feature: str) -> str:
    """
    Get the filename cleaned from the feature.
    """
    return sub(r'[,\/\\\.\(\)]', '', feature).replace(" ", "-").lower()


def main():
    """
    Main entrypoint into the script. This function will take care of going through
    all the features, fetching the content and writing it to a markdown file
    accordingly.
    """
    FILES_DIR = path.join("docs", "features", "content")

    features = get_features()
    print(f"==> Iterating through {len(features)} for getting content")

    i = 0
    while i < len(features):
        feature = features[i]
        FILE_PATH = path.join(FILES_DIR, f"{get_filename(feature)}.md")

        print("==> Getting content for feature: `", feature, "`")
        try:
            content = fetch_content_for_feature(feature, OPENAI_KEY)
        except TooManyRequestsException:
            # Don't increase the counter since we want to retry the same one
            sleep(8)
            continue

        # If `content` is empty, skip it
        if content == "":
            print("==> Received empty content for feature, skipping!")

        with open(FILE_PATH, "w") as WSTREAM:
            WSTREAM.write(content)

        i += 1

    print("==> Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupt received, exiting gracefully!")
