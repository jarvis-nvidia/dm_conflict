import React from 'react';
import { useSupportedLanguages } from '../../hooks/useApi';
import { FileText, Code2 } from 'lucide-react';

const CodeInput = ({ code, setCode, language, setLanguage, filePath, setFilePath }) => {
  const { data: languagesData } = useSupportedLanguages();
  const languages = languagesData?.languages || [
    { name: 'Python', extensions: ['py'] },
    { name: 'JavaScript', extensions: ['js'] },
    { name: 'TypeScript', extensions: ['ts'] },
    { name: 'Java', extensions: ['java'] },
  ];

  const handleLanguageChange = (e) => {
    const selectedLang = e.target.value;
    setLanguage(selectedLang);
    
    // Update file path extension if it exists
    if (filePath) {
      const langData = languages.find(l => l.name.toLowerCase() === selectedLang);
      if (langData && langData.extensions) {
        const baseName = filePath.split('.')[0] || 'temp_file';
        setFilePath(`${baseName}.${langData.extensions[0]}`);
      }
    }
  };

  const codeExamples = {
    python: `def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        return x + y
    
    def divide(self, x, y):
        return x / y  # Potential division by zero`,
    
    javascript: `function calculateSum(a, b) {
    return a + b;
}

class UserManager {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        this.users.push(user);
    }
    
    findUserById(id) {
        for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === id) {
                return this.users[i];
            }
        }
        return null;
    }
}`,
    
    java: `public class Calculator {
    private int result;
    
    public Calculator() {
        this.result = 0;
    }
    
    public int add(int a, int b) {
        return a + b;
    }
    
    public int divide(int a, int b) {
        return a / b; // Potential division by zero
    }
    
    public void complexMethod(int x, int y, int z, int w, int v) {
        if (x > 0) {
            if (y > 0) {
                if (z > 0) {
                    if (w > 0) {
                        System.out.println("Deeply nested");
                    }
                }
            }
        }
    }
}`,
  };

  const loadExample = () => {
    const example = codeExamples[language] || codeExamples.python;
    setCode(example);
    
    const langData = languages.find(l => l.name.toLowerCase() === language);
    if (langData && langData.extensions) {
      setFilePath(`example.${langData.extensions[0]}`);
    }
  };

  return (
    <div className="space-y-4">
      {/* Language and File Path */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Language
          </label>
          <select
            value={language}
            onChange={handleLanguageChange}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            {languages.map((lang) => (
              <option key={lang.name} value={lang.name.toLowerCase()}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            File Path (optional)
          </label>
          <input
            type="text"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="e.g., src/main.py"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Code Textarea */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Code
          </label>
          <button
            onClick={loadExample}
            className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 flex items-center space-x-1"
          >
            <FileText className="w-4 h-4" />
            <span>Load Example</span>
          </button>
        </div>
        
        <div className="relative">
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            className="w-full h-64 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-none"
            style={{ fontFamily: 'Monaco, Consolas, "Lucida Console", monospace' }}
          />
          
          {/* Code icon overlay */}
          <div className="absolute top-2 right-2 text-gray-400">
            <Code2 className="w-4 h-4" />
          </div>
        </div>
        
        <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Lines: {code.split('\n').length} | Characters: {code.length}
        </div>
      </div>
    </div>
  );
};

export default CodeInput;