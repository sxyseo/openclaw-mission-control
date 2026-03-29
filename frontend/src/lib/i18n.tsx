'use client';

import { useEffect, useState } from 'react';
import { IntlProvider } from 'react-intl';
import enMessages from '../locales/en.json';
import zhMessages from '../locales/zh.json';

type Messages = typeof enMessages;
type Locale = 'en' | 'zh';

const messages: Record<Locale, Messages> = {
  en: enMessages as Messages,
  zh: zhMessages as Messages
};

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>('zh');
  const [currentMessages, setCurrentMessages] = useState<Messages>(zhMessages as Messages);

  useEffect(() => {
    // Load locale from localStorage
    const savedLocale = localStorage.getItem('locale') as Locale;
    if (savedLocale && (savedLocale === 'en' || savedLocale === 'zh')) {
      setLocale(savedLocale);
      setCurrentMessages(messages[savedLocale]);
    }
  }, []);

  const changeLocale = (newLocale: Locale) => {
    setLocale(newLocale);
    setCurrentMessages(messages[newLocale]);
    localStorage.setItem('locale', newLocale);
    // Reload the page to apply the new locale
    window.location.reload();
  };

  return (
    <IntlProvider
      key={locale}
      locale={locale}
      messages={currentMessages}
      defaultLocale="en"
    >
      <I18nContext.Provider value={{ locale, changeLocale }}>
        {children}
      </I18nContext.Provider>
    </IntlProvider>
  );
}

import { createContext, useContext } from 'react';

interface I18nContextType {
  locale: Locale;
  changeLocale: (locale: Locale) => void;
}

export const I18nContext = createContext<I18nContextType | undefined>(undefined);

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useI18n must be used within I18nProvider');
  }
  return context;
}

export function useTranslations() {
  const { locale } = useI18n();

  const t = (key: string, values?: Record<string, string | number>) => {
    const keys = key.split('.');
    let value: any = messages[locale];

    for (const k of keys) {
      value = value?.[k];
    }

    if (typeof value === 'string' && values) {
      // Replace placeholders like {name} with actual values
      return value.replace(/\{(\w+)\}/g, (_, match) => values[match]?.toString() || match);
    }

    return value || key;
  };

  return { t, locale };
}
