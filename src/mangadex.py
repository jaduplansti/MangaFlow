import requests;

class MangaDex:
  def __init__(self, debug = False):
    self.base_url = "https://api.mangadex.org";
    self.debug = debug;
  
  def __searchDebug(self, title, mangas):
    if self.debug != True: return;
    
    print(f"fetched {title} at {self.base_url}/manga");
    for manga in mangas:
      print(f"(.) id = {manga["id"]}");
      print(f"(.) attributes = {manga["attributes"].keys()}");
      print("\n");
      
  def search(self, title):
    r = requests.get(
      f"{self.base_url}/manga",
      params = {"title": title},
    );
    mangas = r.json()["data"];
    self.__searchDebug(title, mangas);
    return mangas;
 
  def fetchChapters(self, manga_id):
    r = requests.get(
        f"{self.base_url}/manga/{manga_id}/feed",
        params = {"translatedLanguage[]": ["en"]},
    );
    return [chapter["id"] for chapter in r.json()["data"]];
  
  def fetchImage(self, chapter_id):
    image_urls = [];
    r = requests.get(f"{self.base_url}/at-home/server/{chapter_id}")
    r_json = r.json()

    host = r_json["baseUrl"]
    chapter_hash = r_json["chapter"]["hash"]
    data = r_json["chapter"]["data"]
    data_saver = r_json["chapter"]["dataSaver"]
    
    for page in data:
      image_urls.append(f"{host}/data/{chapter_hash}/{page}");
    return image_urls;
 