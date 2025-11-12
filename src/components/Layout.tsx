import { Moon, Sun, Menu, X } from "lucide-react";
import { NavLink } from "./NavLink";
import { useState } from "react";
import { Button } from "./ui/button";
import { useTheme } from "next-themes";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-50 backdrop-blur-sm bg-card/95">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div
              className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
              onClick={() => navigate('/')}
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
                <Moon className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">SpecSailor</h1>
                <p className="text-xs text-muted-foreground">Navigate User Retention with Precision</p>
              </div>
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              <NavLink
                to="/"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
              >
                Home
              </NavLink>
              <NavLink
                to="/predictions"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
              >
                User Predictions
              </NavLink>
              <NavLink
                to="/performance"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
              >
                Model Performance
              </NavLink>
              <NavLink
                to="/insights"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
              >
                Insights
              </NavLink>
              <NavLink
                to="/upload"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
              >
                Upload Data
              </NavLink>

              {/* Theme Toggle Button */}
              {mounted && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleTheme}
                  className="ml-2"
                  aria-label="Toggle theme"
                >
                  {theme === "dark" ? (
                    <Sun className="h-5 w-5" />
                  ) : (
                    <Moon className="h-5 w-5" />
                  )}
                </Button>
              )}
            </nav>

            {/* Mobile Menu Button and Theme Toggle */}
            <div className="flex items-center gap-2 md:hidden">
              {mounted && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleTheme}
                  aria-label="Toggle theme"
                >
                  {theme === "dark" ? (
                    <Sun className="h-5 w-5" />
                  ) : (
                    <Moon className="h-5 w-5" />
                  )}
                </Button>
              )}
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </Button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <nav className="md:hidden mt-4 pb-2 flex flex-col gap-1 animate-in slide-in-from-top duration-200">
              <NavLink
                to="/"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </NavLink>
              <NavLink
                to="/predictions"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
                onClick={() => setMobileMenuOpen(false)}
              >
                User Predictions
              </NavLink>
              <NavLink
                to="/performance"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
                onClick={() => setMobileMenuOpen(false)}
              >
                Model Performance
              </NavLink>
              <NavLink
                to="/insights"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
                onClick={() => setMobileMenuOpen(false)}
              >
                Insights
              </NavLink>
              <NavLink
                to="/upload"
                className="px-4 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                activeClassName="!text-primary !bg-primary-light"
                onClick={() => setMobileMenuOpen(false)}
              >
                Upload Data
              </NavLink>
            </nav>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        {children}
      </main>
    </div>
  );
};
