import { Moon } from "lucide-react";
import { NavLink } from "./NavLink";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
                <Moon className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">Barakah Retain</h1>
                <p className="text-xs text-muted-foreground">Islamic App Retention System</p>
              </div>
            </div>
            
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
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        {children}
      </main>
    </div>
  );
};
