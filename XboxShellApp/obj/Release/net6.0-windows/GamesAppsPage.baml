   M S B A M L   `   `   `  ���� G  CXboxShellApp, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null+clr-namespace:XboxShellAppXboxShellApp       XboxShellApp.GamesAppsPage   W SPresentationCore, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     R NSystem.Xaml, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     ,localclr-namespace:XboxShellApp     .���   � ColumnDefinitions  �� $	��325 ��� $��* �.+��� $��0�����#18326a$��Stretch=�.+��� -    ��Name$ BackToDashboardBtn��$��⟵ Back��$	��110��$��40��$��
18,24,0,18q�$��16(�
����������#2d7dff
������ $
��Left=��� -    ��Name$ StoragePanel��$��0,36,0,0q��� $��0,40,0,0q�.+��� $��Library��
�������$
��Bold"�$��18(�$��	36,12,0,4q��� $��	18,12,0,0q�.+��� -   $ GamesBtn��$��Games��$��0,4,0,0q�$��16(����#2298fc
��������� -   $ AppsBtn��$
��Apps��$��0,4,0,0q�$��16(����#2298fc
��������� -   $ MusicBtn��$��Music��$��0,4,0,0q�$��16(����#2298fc
��������� -   $ PicturesBtn��$��Pictures��$��0,4,0,0q�$��16(����#2298fc
��������� -   $ 	VideosBtn��$��Videos��$��0,4,0,0q�$��16(����#2298fc
�������� $��1�� � RowDefinitions �� $
��Auto ��� $��* �.+���  �� Orientation$ 
Horizontal=�$��
38,34,0,16q�$��0��$
��Left=�.+��� -    ��Name$ AZSortCombo��$��90��$��36��$��0,0,10,0q�.@��� $	��A-Z���� $	��Z-A���� -	   $ DriveSortCombo��$	��150��$��36��$��0,0,10,0q�.@��� $��
All Drives���� -
   $ MostPlayedCombo��$	��110��$��36��$��0,0,10,0q�.@��� $��Most Played���� $��Least Played���� -   $ 
GenreCombo��$��90��$��36��$��0,0,10,0q�.@��� $��
All Genres���� $��1��$��
18,0,18,18q�$
��Auto=�.���� -    ��Name$ TilesItemsControl������ .R�A�  A� Columns$ 7������ .R�   XboxShellApp.GameAppTile     XboxShellApp.GameAppTile   TileClicked Tile_TileClicked