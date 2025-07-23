import React, { useState } from "react";
import "./App.css";
import { ThemeProvider } from './contexts/ThemeContext';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import CodeAnalyzer from './components/CodeAnalysis/CodeAnalyzer';
import CodeSmellDashboard from './components/CodeSmells/CodeSmellDashboard';
import LearningDashboard from './components/Learning/LearningDashboard';
import GitHubImport from './components/GitHub/GitHubImport';

function App() {
  const [activeTab, setActiveTab] = useState('analysis');

  const renderContent = () => {
    switch (activeTab) {
      case 'analysis':
        return <CodeAnalyzer />;
      case 'smells':
        return <CodeSmellDashboard />;
      case 'learning':
        return <LearningDashboard />;
      case 'github':
        return <GitHubImport />;
      default:
        return <CodeAnalyzer />;
    }
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
        <Header activeTab={activeTab} onTabChange={setActiveTab} />
        <main className="flex-1">
          {renderContent()}
        </main>
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App;
