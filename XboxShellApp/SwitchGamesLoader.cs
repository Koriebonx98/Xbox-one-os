using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;

namespace XboxShellApp
{
    public class SwitchGame
    {
        public string TitleID { get; set; }
        public string Name { get; set; }
        public string Genre { get; set; }
        public string Publisher { get; set; }
        public string ReleaseDate { get; set; }
    }

    public static class SwitchGamesLoader
    {
        public static List<SwitchGame> LoadSwitchGames()
        {
            string jsonPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data", "Switch.Games.Json");
            
            if (!File.Exists(jsonPath))
            {
                return new List<SwitchGame>();
            }

            try
            {
                string json = File.ReadAllText(jsonPath);
                var games = JsonSerializer.Deserialize<List<SwitchGame>>(json);
                return games ?? new List<SwitchGame>();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error loading Switch games: {ex.Message}");
                return new List<SwitchGame>();
            }
        }

        public static void CreateGameFiles()
        {
            var games = LoadSwitchGames();
            string gamesDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data", "Nintendo - Switch", "Games");
            
            if (!Directory.Exists(gamesDir))
            {
                Directory.CreateDirectory(gamesDir);
            }

            foreach (var game in games)
            {
                string gameFilePath = Path.Combine(gamesDir, game.TitleID);
                
                try
                {
                    // Write game name and metadata to the file
                    string content = $"{game.Name}\n" +
                                   $"Title ID: {game.TitleID}\n" +
                                   $"Genre: {game.Genre}\n" +
                                   $"Publisher: {game.Publisher}\n" +
                                   $"Release Date: {game.ReleaseDate}";
                    
                    File.WriteAllText(gameFilePath, content);
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine($"Error creating game file for {game.Name}: {ex.Message}");
                }
            }
        }
    }
}
