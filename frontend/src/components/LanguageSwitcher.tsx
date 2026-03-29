'use client';

import { useState, useTransition } from 'react';
import { useI18n } from '@/lib/i18n';

const locales = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'zh', name: '中文', flag: '🇨🇳' }
] as const;

export default function LanguageSwitcher() {
  const { locale, changeLocale } = useI18n();
  const [isPending, startTransition] = useTransition();
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (newLocale: 'en' | 'zh') => {
    startTransition(() => {
      changeLocale(newLocale);
      setIsOpen(false);
    });
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        aria-label="Change language"
      >
        <span className="text-lg">{locales.find(l => l.code === locale)?.flag}</span>
        <span className="text-sm font-medium">{locales.find(l => l.code === locale)?.name}</span>
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 z-50">
          {locales.map((loc) => (
            <button
              key={loc.code}
              onClick={() => handleChange(loc.code)}
              disabled={isPending}
              className={`w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors first:rounded-t-md last:rounded-b-md flex items-center gap-2 ${
                locale === loc.code ? 'bg-gray-100 dark:bg-gray-700' : ''
              }`}
            >
              <span className="text-lg">{loc.flag}</span>
              <span className="text-sm">{loc.name}</span>
              {locale === loc.code && (
                <svg
                  className="w-4 h-4 ml-auto text-blue-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
