import React from 'react';
import { Heart, Code2, Github, ExternalLink } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                DEV<span className="text-blue-500">MIND</span>
              </h3>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-sm max-w-md">
              AI-powered development assistant that helps you write better code, detect issues, 
              and learn from patterns. Built for developers, by developers.
            </p>
          </div>

          {/* Features */}
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Features</h4>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li className="flex items-center space-x-2">
                <Code2 className="w-4 h-4" />
                <span>Code Analysis</span>
              </li>
              <li className="flex items-center space-x-2">
                <Code2 className="w-4 h-4" />
                <span>Smell Detection</span>
              </li>
              <li className="flex items-center space-x-2">
                <Code2 className="w-4 h-4" />
                <span>Learning System</span>
              </li>
              <li className="flex items-center space-x-2">
                <Github className="w-4 h-4" />
                <span>GitHub Integration</span>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>
                <a href="#" className="hover:text-blue-500 flex items-center space-x-1">
                  <span>Documentation</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-blue-500 flex items-center space-x-1">
                  <span>API Reference</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-blue-500 flex items-center space-x-1">
                  <span>VSCode Extension</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-blue-500 flex items-center space-x-1">
                  <span>Community</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom section */}
        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
              <span>© {currentYear} DevMind AI. All rights reserved.</span>
            </div>
            
            <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
              <span className="flex items-center space-x-1">
                <span>Made with</span>
                <Heart className="w-4 h-4 text-red-500" />
                <span>for developers</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;