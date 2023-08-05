
def createStandardizedDF(inputDF, DFtype):
    exec("columnNames_dict=" + DFtype + "_columnNames_dict", locals(), globals())

    exec("columns=" + DFtype + "_columns", locals(), globals())

    exec("outputDF=" + inputDF + ".rename(columns=" + DFtype + "_columnNames_dict)", locals(), globals())

    for i in columns:
        if i not in outputDF.columns:
            outputDF[i] = pd.np.nan

    outputDF_final = outputDF[columns]

    return outputDF_final


### test
### DICTIONARIES OF ORIGINAL COLUMNS AND ITS NAMES WITH PROJECT CONVENTION
shops_columnNames_dict = {"id": "shopId"
    , "slug": "shopSlug"
    , "name": "shopName"
    , "homepage": "shopHomepage"
    , "rating": "rating"
    , "is_certified_seller": "certifiedSeller"
    , "review_count": "reviewCount"
    , "rating_count": "ratingCount"
    , "verified_by_customers_status.name": "verifiedByCustomers_status"
    , "has_cashback_guarantee": "cashbackGuarantee"}

shops_columnTypes_dict = {"shopId": "Int64"
    , "rating": "Int64"
    , "certifiedSeller": "bool"
    , "reviewCount": "Int64"
    , "ratingCount": "Int64"
    , "cashbackGuarantee": "bool"
    , "date": "datetime64"
                          }

offers_columnNames_dict = {"shop_id": "shopId"
    , "offer.id": "offerId"
    , "offer.item_id": "shopProductId"
    , "offer.name": "offerName"
    , "offer.price": "price"
    , "offer.average_delivery_days": "delivery_averageDays"
    , "offer.gifts": "gifts"
    , "offer.shopping_cart": "shoppingCart"
    , "offer.min_delivery_price": "delivery_minPrice"
    , "offer.attributes": "attributes"
    , "offer.availability.type": "availability"
    , "offer.index_variant": "index_variant"}

offers_columnTypes_dict = {"shopId": "Int64"
    , "offerId": "Int64"
    , "shoppingCart": "bool"
    , "price": "float64"
    , "offer_position": "Int64"
    , "delivery_averageDays": "float64"
    , "delivery_minPrice": "float64"
    , "productId_heureka": "Int64"
    , "index_variant": "Int64"
    , "date": "datetime64"
                           }

products_columnNames_dict = {"product.id": "productId_heureka"
    , "product.name": "productName"
    , "product.slug": "productSlug"
    , "product.rating.rating": "product_rating_score"
    , "product.rating.rating_count": "product_rating_count"
    , "product.rating.review_count": "product_rating_reviewCount"
    , "product.category.id": "categoryId"
    , "product.category.name": "categoryName"
    , "product.category.slug": "categorySlug"
    , "product.category_position": "categoryPosition"
    , "product.producer.name": "producer"
    , "product.status.name": "status"
    , "product.images": "productImages"
    , "product.offer_attributes": "offerAttributes"
                             }

products_columnTypes_dict = {"productId_heureka": "Int64"
    , "categoryId": "Int64"
    , "product_rating_score": "Int64"
    , "product_rating_count": "Int64"
    , "product_rating_reviewCount": "Int64"
    , "categoryPosition": "Int64"
    , "date": "datetime64"
                             }

shops_SOTYlabel_columnNames_dict = {"id": "shopId"
    , "shop_of_the_year.year": "year"
    , "shop_of_the_year.type.name": "type"
    , "shop_of_the_year.description": "titleName"
                                    }


from pandas import json_normalize
import pandas as pd

tic_general = time.perf_counter()
loop_counter = 1


shops_SOTYlabel_columnTypes_dict = {"shopId": "Int64"
    , "year": "Int64"
    , "date": "datetime64"
                                    }


### LISTS OF COLUMNS FOR OUTPUT TABLES
offers_columns = list(offers_columnNames_dict.values())
shops_columns = list(shops_columnNames_dict.values())
products_columns = list(products_columnNames_dict.values())
shops_SOTYlabel_columns = list(shops_SOTYlabel_columnNames_dict.values()) + ["date"]


for (categoryId, productId) in list(heurekaProductSlugs)[1:100]:
    tic_loop = time.perf_counter()

    try:
        response_json, results = heureka_apiCall(productId, categoryId)
    except (TypeError, KeyError):
        noResult_productIds = noResult_productIds + [(categoryId, productId)]
        continue

    offers_all = pd.DataFrame(columns=list(offers_columnNames_dict.values()) + ["offerLabel"])
    shops_all = pd.DataFrame(columns=list(shops_columnNames_dict.values()))
    ## PRODUCTS_METADATA: RENAME AND EXTRACT ONLY REQUIRED COLUMS
    products_metadata = createStandardizedDF(inputDF="results", DFtype="products")
    products_metadata["date"] = today

    ## OFFERS + SHOPS DATA EXTRACTION
    ## TOP OFFER
    if response_json["result"]["product"]["top_shop"] != None:
        shops_top = json_normalize(response_json["result"]["product"]["top_shop"])
        shops_top = createStandardizedDF(inputDF="shops_top", DFtype="shops")

        offers_top = response_json["result"]["product"]["top_shop"]["offer"]

        offers_top = json_normalize(offers_top)
        offers_top.columns = ["offer." + column for column in offers_top.columns]
        offers_top["shop_id"] = shops_top["shopId"]
        offers_top = createStandardizedDF(inputDF="offers_top", DFtype="offers")
        offers_top["index_variant"] = 0
        offers_top["offerLabel"] = "top"

        offers_all = pd.concat([offers_all, offers_top], axis=0)
        shops_all = pd.concat([shops_all, shops_top], axis=0)

    ## HIGHLIGHTED OFFERS (ONLY WHERE AVAILABLE)
    if results["product.highlighted_shops"][0] != []:
        shops_highlighted = json_normalize(response_json["result"]["product"], record_path="highlighted_shops")
        shops_highlighted = createStandardizedDF(inputDF="shops_highlighted", DFtype="shops")

        offers_highlighted = response_json["result"]["product"]["highlighted_shops"]
        index_offerVariants(offers_highlighted)
        offers_highlighted = json_normalize(offers_highlighted, meta="id", meta_prefix="shop_", record_path="offers",
                                            record_prefix="offer.")

        offers_highlighted = createStandardizedDF(inputDF="offers_highlighted", DFtype="offers")
        offers_highlighted["offerLabel"] = "highlighted"

        offers_all = pd.concat([offers_all, offers_highlighted], axis=0)
        shops_all = pd.concat([shops_all, shops_highlighted], axis=0)

    ## OTHERS OFFERS
    if response_json["result"]["product"]["shops"] != []:
        shops_other = json_normalize(response_json["result"]["product"], record_path="shops")
        shops_other = createStandardizedDF(inputDF="shops_other", DFtype="shops")

        offers_other = response_json["result"]["product"]["shops"]
        index_offerVariants(offers_other)
        offers_other = json_normalize(offers_other, meta="id", meta_prefix="shop_", record_path="offers",
                                      record_prefix="offer.")
        offers_other = createStandardizedDF(inputDF="offers_other", DFtype="offers")
        offers_other["offerLabel"] = "others"

        offers_all = pd.concat([offers_all, offers_other], axis=0)
        shops_all = pd.concat([shops_all, shops_other], axis=0)

    if len(offers_all) != 0:
        offers_all["offer_position"] = (offers_all[["index_variant"]] == 0).cumsum()
        offers_all["productId_heureka"] = response_json["result"]["product"]["id"]
        offers_all["productId_heureka"] = offers_all["productId_heureka"].astype('Int64')
        offers_all["date"] = today

    if "shop_of_the_year.year" in json_normalize(response_json["result"]["product"]["shops"]).columns:
        shops_SOTYlabel = json_normalize(response_json["result"]["product"]["shops"])
        shops_SOTYlabel = createStandardizedDF(inputDF="shops_SOTYlabel", DFtype="shops_SOTYlabel")
        shops_SOTYlabel = shops_SOTYlabel[pd.notnull(shops_SOTYlabel["year"])]
        try:
            out_shop_SOTYlabel = pd.concat([out_shop_SOTYlabel, shops_SOTYlabel], axis=0)
        except NameError:
            out_shop_SOTYlabel = shops_SOTYlabel
        # shops_SOTYlabel_output=pd.concat([shops_SOTYlabel_output,shops_SOTYlabel],axis=0)

    try:
        out_product_offers = pd.concat([out_product_offers, offers_all], axis=0)
    except NameError:
        out_product_offers = offers_all

    try:
        out_product_products = pd.concat([out_product_products, products_metadata], axis=0)
    except NameError:
        out_product_products = products_metadata

    try:
        out_shop_shops = pd.concat([out_shop_shops, shops_all], axis=0)
    except NameError:
        out_shop_shops = shops_all

    toc_loop = time.perf_counter()
    print(
        f"Loop counter: {loop_counter} /n Loop parsed in {toc_loop - tic_loop:0.4f} seconds,/n total in {toc_loop - tic_general:0.4f} /n on average {(toc_loop - tic_general) / loop_counter:0.4f}")
    loop_counter = loop_counter + 1


##############################################################



out_shop_shops = out_shop_shops.drop_duplicates(subset=["shopId"], keep="first")
out_shop_shops["date"] = today

out_shop_SOTYlabel = (out_shop_SOTYlabel[pd.notnull(out_shop_SOTYlabel["year"])]
                      .drop_duplicates(subset=["shopId"], keep="first"))

out_shop_SOTYlabel["date"] = out_shop_SOTYlabel["date"].fillna(today)

out_product_products = out_product_products.astype(products_columnTypes_dict)
out_shop_shops = out_shop_shops.astype(shops_columnTypes_dict)
out_product_offers = out_product_offers.astype(offers_columnTypes_dict)
out_shop_SOTYlabel = out_shop_SOTYlabel.astype(shops_SOTYlabel_columnTypes_dict)

toc_general = time.perf_counter()
print(
    f"Process finished in  {toc_general - tic_general:0.4f} seconds total in /n on average {(toc_general - tic_general) / loop_counter:0.4f}")

############################################################

print("FINISHED - PHASE 3a: MAIN CODE - DATA EXTRACTION")

# ## EXTRACTION STATISTICS
print("PHASE 3b: MAIN CODE - Extraction Statistics")
print("=============================================")
print("Missing Product Ids:")
print("Count:{}".format(len(noResult_productIds)))
print("List:{}".format(noResult_productIds))
print("---------------------------------------------")
print("Extracted Product Ids:")
print("Count:{}".format(len(out_product_products)))
print("---------------------------------------------")
print("Shops:")
print("Count:{}".format(len(out_shop_shops)))
print("---------------------------------------------")
print("Offers:")
print("Count:{}".format(len(out_product_offers)))
print("---------------------------------------------")
print("Shop of the Year:")
print("Count:{}".format(len(out_shop_SOTYlabel)))
print("FINISHED - PHASE 3b: MAIN CODE - Extraction STATISTICS")


