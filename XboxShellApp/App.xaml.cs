using System.Windows;
using System.Net;

namespace XboxShellApp
{
    public partial class App : Application
    {
        // User-Agent string for HTTP requests made by the application
        private const string UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 GameOS/1.0";
        
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            
            // Configure system proxy for HTTP requests
            WebRequest.DefaultWebProxy = WebRequest.GetSystemWebProxy();
            
            // Configure User-Agent for HTTP image requests
            // Note: This uses reflection to set the default User-Agent for WebRequest because
            // WPF's Image control uses WebRequest internally and there's no supported API to set the User-Agent otherwise.
            // This may break in future .NET versions if the internal field name changes.
            var userAgentField = typeof(WebRequest).GetField("s_DefaultUserAgent", 
                System.Reflection.BindingFlags.Static | System.Reflection.BindingFlags.NonPublic);
            
            if (userAgentField != null)
            {
                userAgentField.SetValue(null, UserAgent);
            }
            // If the field is not found, the application will still work but may not send a User-Agent header
        }
    }
}
