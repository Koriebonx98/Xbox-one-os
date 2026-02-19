using System.Windows;
using System.Net;

namespace XboxShellApp
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            
            // Configure system proxy for HTTP requests
            WebRequest.DefaultWebProxy = WebRequest.GetSystemWebProxy();
            
            // Configure User-Agent for HTTP image requests
            // Using reflection to set the default User-Agent for WebRequest
            var userAgentField = typeof(WebRequest).GetField("s_DefaultUserAgent", 
                System.Reflection.BindingFlags.Static | System.Reflection.BindingFlags.NonPublic);
            
            if (userAgentField != null)
            {
                userAgentField.SetValue(null, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 GameOS/1.0");
            }
        }
    }
}
