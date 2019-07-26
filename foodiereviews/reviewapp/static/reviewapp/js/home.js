function getRestaurants(categoryId){
    var endpoint = "/reviewapp/api/restaurants/list/";

    $.ajax({
        method: "GET",
        url: endpoint,
        data: {
            category_id: categoryId,
        },
        success: function(data) {
            if (data.restaurants){
                changeCategoryBackground(categoryId);
                displayRestaurants(data.restaurants);
            }
        }
    });
}
function changeCategoryBackground(categoryId){
    imageURL = "url('/static/reviewapp/images/cat"+categoryId+".jpg')";
    $('#category-banner').css("background-image", imageURL); 
}

function displayRestaurants(restaurants){
    console.log(restaurants);
    var restaurantsDiv = $("#restaurants-list");
    restaurantsDiv.empty();

    if (!restaurants.length){
        $("#none-found").fadeIn('slow');
        return;
    }

    $("#none-found").hide();
    restaurants.forEach(restaurant => {
        var newRestaurant = $("#newRestaurant").clone().removeAttr("id");
        newRestaurant.find("span.restaurant-id").text(restaurant.id);
        newRestaurant.find("span.restaurant-text").text(restaurant.restaurant_text);
        newRestaurant.find("span.address").text(restaurant.restaurant_address);
        newRestaurant.find("span.reviews").text(restaurant.review_amount);
        newRestaurant.find("span.category").text(restaurant.category);
        createStarRatings(newRestaurant.find("span.rating"), restaurant.rating);
        createPriceRatings(newRestaurant.find("span.pricing"), restaurant.pricing);
        var imgsrc = "/static/reviewapp/images/" + restaurant.id + ".jpg";
        newRestaurant.find("img").attr("src", imgsrc);
        var ahref = "/reviewapp/resto/" + restaurant.id + "/";
        newRestaurant.find("a").attr("href", ahref);
        newRestaurant.show();
        restaurantsDiv.prepend(newRestaurant[0]).hide().fadeIn('slow');
    });
}
function createStarRatings(ratingSpan , number){
    for (var i = 0; i < parseInt(number); i++) {
        ratingSpan.append('<i class="fas fa-star"/></i>');
    }
}
function createPriceRatings(priceSpan , number){
    for (var i = 0; i < parseInt(number); i++) {
        priceSpan.append('<i class="fas fa-dollar-sign"></i>');
    }
}