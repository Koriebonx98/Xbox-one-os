using System.Windows;
using System.Windows.Controls;
using System.Diagnostics;

namespace XboxShellApp
{
    public partial class SettingsPage : UserControl
    {
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
                var emailAddress = "Koriegrant@icloud.com";
                var subject = "Inquiry";
                var mailtoUrl = $"mailto:{emailAddress}?subject={subject}";
                Process.Start(new ProcessStartInfo
                {
                    FileName = mailtoUrl,
                    UseShellExecute = true
                });
            }
            catch
            {
                // Silently fail if no email client is configured
            }
        }
    }
}
