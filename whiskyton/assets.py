from flask_assets import Bundle

BUNDLES = {
    "style": Bundle(
        "scss/header.scss",
        "scss/search.scss",
        "scss/whisky_card.scss",
        "scss/footer.scss",
        "scss/autocomplete.scss",
        "scss/404.scss",
        output="css/style.min.css",
        filters="pyscss",
    )
}
