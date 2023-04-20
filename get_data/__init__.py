from bs4 import BeautifulSoup
import requests
import pandas as pd
# urls = "https://www.airlinequality.com/airline-reviews/british-airways"

data = []
pages = 355
for i in range(1, pages):
    page = f"https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/"
    airways = requests.get(page).content
    soup = BeautifulSoup(airways, 'html.parser')

    articles = soup.findAll('article', {'itemtype': 'http://schema.org/Review'})
    for article in articles:
        review_data = dict()
        review_data["Title"] = article.find('h2', {'class': 'text_header'}).text
        print(review_data["Title"])

        reviews = article.find('div', {'itemprop': 'reviewBody'})
        comment = reviews.text
        if "✅ Trip Verified" in comment:
            review_data["Review"] = comment.split("|")[1].strip()
            review_data["Isverfi"] = comment.split("|")[0].replace("✅ ", '').strip()

        elif "Not Verified" in comment:
            review_data["Review"] = comment.split("|")[1].strip()
            review_data["Isverfi"] = comment.split("|")[0].strip()

        else:
            review_data["Review"] = comment.strip()

        # Overall ratings
        ratings = article.find('div', {'itemprop': 'reviewRating'})
        if ratings:
            review_data["Ratings"] = ratings.find('span').text

        #get all ratings
        tables = article.find('table', {'class': 'review-ratings'})

        #get aircraft kode, left NaN if nothing
        aircraft = tables.find('td', {'class': 'review-rating-header aircraft'})
        if aircraft:
            review_data["Aircraft Type"] = aircraft.find_next_sibling('td', {'class': 'review-value'}).text

        else:
            print("Aircraft type is NaN")

        traveller = tables.find('td', {'class': 'review-rating-header type_of_traveller'})
        if traveller:
            review_data["Traveler Type"] = traveller.find_next_sibling('td', {'class': 'review-value'}).text

        else:
            print("Traveler type is Nan")

        # Route with departure and arrive
        routes = tables.find('td', {'class': 'review-rating-header route'})
        if routes:
            value_routes = routes.find_next_sibling('td', {'class': 'review-value'}).text
            review_data["Route"] = value_routes

        else:
            print("Route is NaN")

        # Date flight
        flight = tables.find('td', {'class': 'review-rating-header date_flown'})
        if flight:
            review_data["Date"] = flight.find_next_sibling('td', {'class': 'review-value'}).text

        else:
            print("Date Flight is NaN")

        # Seat Comfortable
        seat = tables.find('td', {'class': 'review-rating-header seat_comfort'})
        if seat:
            seat_star = seat.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            seat_value = seat_star.findAll('span', {'class': 'star fill'})
            review_data["Seat Ratings"] = len(seat_value)

        else:
            print('seat rating is NaN')

        # Staff Service
        service = tables.find('td', {'class': 'review-rating-header cabin_staff_service'})
        if service:
            service_star = service.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            service_value = service_star.findAll('span', {'class': 'star fill'})
            review_data["Staff Ratings"] = len(service_value)

        else:
            print("service ratings is NaN")

        # Food Service and beverages
        foods = tables.find('td', {'class': 'review-rating-header food_and_beverages'})
        if foods:
            foods_star = foods.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            foods_value = foods_star.findAll('span', {'class': 'star fill'})
            review_data["Food Ratings"] = len(foods_value)

        else:
            print("foods ratings is NaN")

        # Inflight entertainment
        entertainment = tables.find('td', {'class': 'review-rating-header inflight_entertainment'})
        if entertainment:
            entertainment_star = entertainment.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            entertainment_value = entertainment_star.findAll('span', {'class': 'star fill'})
            review_data["Entertainments Ratings"] = len(entertainment_value)

        else:
            print("Inflight Entertainments ratings is NaN")

        # Ground Service
        ground_s = tables.find('td', {'class': 'review-rating-header ground_service'})
        if ground_s:
            ground_s_star = ground_s.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            ground_s_value = ground_s_star.findAll('span', {'class': 'star fill'})
            review_data["Ground Service Ratings"] =len(ground_s_value)

        else:
            print("ground service ratings is NaN")

        # Free Wifi ratings
        wifis = tables.find('td', {'class': 'review-rating-header wifi_and_connectivity'})
        if wifis:
            wifis_star = wifis.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            wifis_value = wifis_star.findAll('span', {'class': 'star fill'})
            review_data["Wifi Ratings"] = len(wifis_value)

        else:
            print("Wifis ratings is NaN")

        # Value for Money ratings
        money = tables.find('td', {'class': 'review-rating-header value_for_money'})
        if money:
            money_star = money.find_next_sibling('td', {'class': 'review-rating-stars stars'})
            money_value = money_star.findAll('span', {'class': 'star fill'})
            review_data["Value For Money Ratings"] = len(money_value)
        else:
            print("value for money ratings is NaN")

        # recommended
        recomend = tables.find('td', {'class': 'review-rating-header recommended'})
        if recomend:
            review_data["Recomended"] = recomend.find_next_sibling('td').text

        else:
            print("Recomended ratings is NaN")

        data.append(review_data)
        print("-"*50)
    print(f"get page : {i}")

df = pd.DataFrame(data)

# Save the dataframe to a CSV file
df.to_csv('reviews.csv', encoding='utf-8', index=False, sep='|')

