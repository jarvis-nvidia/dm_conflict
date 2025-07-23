import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-[#111418] border-t border-[#283039] px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="text-sm text-[#9cabba]">
          © 2024 EV MIND. All rights reserved.
        </div>
        <div className="flex space-x-4 text-sm text-[#9cabba]">
          <a href="#" className="hover:text-white transition-colors">
            Privacy Policy
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Terms of Service
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;