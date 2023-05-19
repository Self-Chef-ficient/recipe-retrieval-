# recipe-retrieval-api

## Building Docker image

docker build -t recipe-retrieval .

## Run docker image

docker run -d recipe-retrieval 

Do a POST request on 127.0.0.1:5000/getRecipe with data in below format to get a response

## Sample Input

curl --location 'http://127.0.0.1:5000/getRecipe' --form 'file=@"1.jpg"'

## Sample Output

[
    {
        "Recipe": 1,
        "Title": "Garlic shrimp scampi",
        "Ingredients": "shrimp, pepper, butter, clove, oil, salt, pasta, parsley",
        "Instructions": "Heat olive oil in a large skillet over medium heat.-Cook and stir garlic in hot oil until fragrant, about 1 minute.-Stir shrimp into garlic; cook and stir until shrimp are pink and opaque, about 3 minutes.-Season with salt and pepper.-Stir butter into shrimp mixture until melted and sauce is heated through, about 2 minutes.-Stir parsley into shrimp mixture; cook and stir until heated through, about 1 minute."
    },
    {
        "Recipe": 2,
        "Title": "Pasta and shrimp",
        "Ingredients": "shrimp, pepper, butter, clove, oil, salt, pasta, parsley",
        "Instructions": "Cook pasta in water according to package directions.-Meanwhile, heat oil in large skillet over medium-high heat.-Add garlic, parsley, salt and pepper.-Cook and stir 2-3 minutes.-Add shrimp; cook 3-4 minutes.-Add butter, cook and stir 1-2 minutes or just until butter is melted.-Drain pasta.-Add pasta to skillet; toss to coat."
    },
    {
        "Recipe": 3,
        "Title": "Garlic angel hair with shrimp",
        "Ingredients": "shrimp, pepper, butter, clove, oil, salt, pasta, parsley",
        "Instructions": "Place butter in heavy large skillet or dutch oven.-Heat over high heat until it melts and begins to foam, about 2 minutes.-Stir in garlic and cook until garlic turns golden, about 1 minute.-Reduce heat to medium.-Add shrimp and cook until just opaque throughout, 2 to 3 minutes.-Remove from heat and season with pepper.-Add angel hair pasta to pan and toss until heated through and beginning to wilt, about 2 minutes.-Season with salt and pepper.-Sprinkle with parsley, if desired.-Serve immediately."
    },
    {
        "Recipe": 4,
        "Title": "Fettuccine with shrimp",
        "Ingredients": "shrimp, pepper, butter, clove, oil, salt, pasta, parsley",
        "Instructions": "Cook pasta according to package directions.-Meanwhile, heat olive oil in a large skillet over medium-high heat.-Stir in crushed red pepper, and garlic; cook and stir until the garlic begins to sizzle and turns fragrant, 2 to 3 minutes.-Toss shrimp and garlic mixture with pasta.-Season with salt, black pepper, and parsley."
    }
]
