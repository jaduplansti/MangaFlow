import flet as ft
from mangaflow import MangaFlow;

def main(page):
  mangaflow = MangaFlow(page);
 
  
ft.app(target = main, view = ft.AppView.WEB_BROWSER, port = 8500);
