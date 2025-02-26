import "./globals.css";
import "@mantine/core/styles.css";

import React from "react";
import {
  MantineProvider,
  ColorSchemeScript,
  mantineHtmlProps,
} from "@mantine/core";
import { theme } from "../../theme";

import { HeaderTabs } from "./_components/HeaderTabs";
import { FooterLinks } from "./_components/FooterLinks";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" {...mantineHtmlProps}>
      <head>
        <meta charSet="utf-8" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
        <ColorSchemeScript />
      </head>
      <body>
        <MantineProvider defaultColorScheme="dark" theme={theme}>
          <HeaderTabs />
          {children}
          <FooterLinks />
        </MantineProvider>
      </body>
    </html>
  );
}
