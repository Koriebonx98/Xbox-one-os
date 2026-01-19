using System;
using System.Windows;
using System.Windows.Controls;
using System.Diagnostics;

namespace XboxShellApp
{
    public partial class SettingsPage : UserControl
    {
        private const string CONTACT_EMAIL = "Koriegrant@icloud.com";
        private const string EMAIL_SUBJECT = "Inquiry";
        private MainWindow _mainWindow;

        public SettingsPage(MainWindow mainWindow)
        {
            InitializeComponent();
            _mainWindow = mainWindow;
            BackToDashboardBtn.Click += (s, e) => _mainWindow.SwitchToDashboard();
            EmailContactBtn.Click += EmailContactBtn_Click;
        }

        private void EmailContactBtn_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var mailtoUrl = $"mailto:{CONTACT_EMAIL}?subject={EMAIL_SUBJECT}";
                Process.Start(new ProcessStartInfo
                {
                    FileName = mailtoUrl,
                    UseShellExecute = true
                });
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Failed to open email client: {ex.Message}");
                // Silently fail if no email client is configured
            }
        }
    }
}
