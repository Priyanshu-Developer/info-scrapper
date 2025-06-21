from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_insta_without_browser(username):
    url = f"https://insta-stories-viewer.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch page. Status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        nickname = soup.find("h1").text.strip().replace("                   \n(Anonymous profile view)", "")

        post = soup.find("span", class_="profile__stats-posts").text.strip()

        followers = soup.find("span", class_="profile__stats-followers")
        followers = followers.text.strip() if followers else None

        following = soup.find("span", class_="profile__stats-follows")
        following = following.text.strip() if following else None

        desc = soup.find("div", class_="profile__description")
        desc = desc.text.strip() if desc else None

        image = soup.find("img", class_="profile__avatar-pic")
        image = image["src"] if image else None

        return {
            "nickname": nickname,
            "post_count": post,
            "followers_count": followers,
            "following_count": following,
            "profile_description": desc,
            "profile_photo_url": image
        }

    except Exception as e:
        return {"error": f"Parsing failed: {str(e)}"}

@app.route("/scrape", methods=["GET"])
def scrape():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Missing 'username' parameter"}), 400

    data = scrape_insta_without_browser(username)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
