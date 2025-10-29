from mangadex import MangaDex;
import flet as ft;

class MangaFlow:
  def __init__(self, page):
    self.page = page;
    self.mangadex = MangaDex(True);
    self.recently_read_ref = ft.Ref[ft.Column]();
    
    self.search_view_ref = ft.Ref[ft.Column]();
    self.page.theme_mode = ft.ThemeMode.LIGHT;
    self.page.on_route_change = self.onRouteChange;
    
    self.createBottomAppBar();
    self.page.go("/home");
    
  def onRouteChange(self, e):
    self.page.views.clear();
    if e.route == "/home": 
      self.page.views.append(ft.View(
        "/home",
        [self.createBottomAppBar(), self.createDashboard()]
      ));
    elif e.route == "/search":
      self.page.views.append(ft.View(
        "/search",
        [self.createBottomAppBar(), self.createSearch()]
      ));
    self.page.update();
    
  def createBottomAppBar(self):
    return ft.BottomAppBar(
      bgcolor = ft.Colors.CYAN_700,
      shape = ft.NotchShape.CIRCULAR,
      content = ft.Row([
        ft.IconButton(icon = ft.Icons.HOME, on_click = lambda e: self.page.go("/home")),
        ft.Container(expand = True),
        ft.IconButton(icon = ft.Icons.SEARCH, on_click = lambda e: self.page.go("/search")),
        ft.Container(expand = True),
        ft.IconButton(icon = ft.Icons.PEOPLE),
      ],
        alignment = ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment = ft.CrossAxisAlignment.CENTER
      ),
    );
    
  def createDashboard(self):
    return ft.Column(
      [
        ft.Text(
          "Recently Read", 
          size = 18, 
          weight = "bold", 
          color = "#333333"
        ),
        ft.Divider(
          height = 12, 
          thickness = 2, 
          color = "#AAAAAA"
        ),
        ft.Column(
          ref = self.recently_read_ref,
          spacing = 8, 
          scroll = ft.ScrollMode.AUTO,
        ),
      ],
      scroll = ft.ScrollMode.AUTO,
      spacing = 12, 
      alignment = "start",
    );
  
  def createSearch(self, e = None):
    return ft.Column([
      ft.TextField(
        on_submit = self.search,
        hint_text = "Search Manga Here..",
        prefix_icon = ft.Icons.SEARCH,
        border_radius = 20,
        bgcolor = ft.Colors.CYAN_50,
        border_color = ft.Colors.CYAN_200,
        focused_border_color = ft.Colors.CYAN_400),
      ft.Container(expand = True, content = ft.Column(ref = self.search_view_ref, scroll = ft.ScrollMode.ALWAYS))
    ], expand = True);
    
  def updateSearchView(self, titles):
    self.search_view_ref.current.controls.clear();
    for title in titles:
      self.search_view_ref.current.controls.append(
        ft.Container(
          expand = True,
          content = ft.TextButton(
            title,
            expand = True,
            icon = ft.Icons.BOOK,
            url = "/read",
            style = ft.ButtonStyle(
              padding = 12,
              shape = ft.RoundedRectangleBorder(radius = 14),
              bgcolor = ft.Colors.CYAN_50,
              overlay_color = ft.Colors.CYAN_100,  # hover/tap effect
              text_style = ft.TextStyle(
                color = ft.Colors.CYAN_900,
                size = 14,
                weight = "bold",
              ),
            ),
          ),
          border_radius = 14,
          bgcolor = ft.Colors.CYAN_200,
          padding = 2,
        )
      );
    self.page.update();
  
  def search(self, e):
    title = e.control.value;
    titles = [];
    results = self.mangadex.search(title);
    for manga in results:
      language = list(manga["attributes"]["title"])[0];
      titles.append(manga["attributes"]["title"][language]);
    print(titles);
    self.updateSearchView(titles);
  
  