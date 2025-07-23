import React from 'react';
import { Bell, User } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

const Header = ({ activeTab, onTabChange }) => {
  const navItems = [
    { id: 'analysis', label: 'Code Analysis' },
    { id: 'smells', label: 'Code Smells' },
    { id: 'learning', label: 'Learning Dashboard' },
    { id: 'github', label: 'GitHub Integration' }
  ];

  return (
    <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#283039] px-10 py-3 bg-[#111418]">
      <div className="flex items-center gap-4 text-white">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-center bg-no-repeat aspect-square bg-cover rounded-lg"
               style={{backgroundImage: "url('https://images.unsplash.com/photo-1744324472890-d4cac1650e2e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwyfHxnZW9tZXRyaWMlMjBicmFpbnxlbnwwfHx8fDE3NTMyOTA4NjF8MA&ixlib=rb-4.1.0&q=85')"}}>
          </div>
          <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">EV MIND</h2>
        </div>
      </div>
      
      <div className="flex flex-1 justify-end gap-8">
        <div className="flex items-center gap-9">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`text-sm font-medium leading-normal transition-colors ${
                activeTab === item.id 
                  ? 'text-white border-b-2 border-b-white pb-2' 
                  : 'text-[#9cabba] hover:text-white'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
        
        <div className="flex items-center gap-3">
          <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 bg-[#283039] text-white gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0 px-2.5 hover:bg-[#3b4754] transition-colors">
            <Bell className="w-5 h-5" />
          </button>
          
          <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 bg-gray-500 flex items-center justify-center">
            <User className="w-6 h-6 text-white" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;