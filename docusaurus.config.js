// @ts-check
const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics – Essentials',
  tagline: 'Professional AI-native textbook with integrated RAG chatbot',
  favicon: 'img/favicon.ico',
  url: 'https://your-username.github.io',
  baseUrl: '/mybook/',
  organizationName: 'your-username',
  projectName: 'mybook',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/mybook/tree/main/',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/your-username/mybook',
          label: 'GitHub',
          position: 'right',
        },
      ],
      style: 'dark',
      hideOnScroll: true,
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Courses',
          items: [
            {
              label: 'Physical AI Fundamentals',
              to: '/intro-physical-ai',
            },
            {
              label: 'Humanoid Robotics',
              to: '/humanoid-robotics',
            },
            {
              label: 'ROS 2 Programming',
              to: '/ros2-fundamentals',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-username/mybook',
            },
            {
              label: 'Documentation',
              to: '/docs',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'About',
              href: 'https://github.com/your-username',
            },
          ],
        },
      ],
      copyright: `Copyright © 2024-2025 Physical AI Course. Built with ❤️ using Docusaurus.`,
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'bash', 'javascript', 'typescript', 'yaml', 'xml', 'sql'],
      magicComments: [
        {
          className: 'theme-code-block-highlighted-line',
          line: 'highlight-next-line',
          block: {begin: 'highlight-start', end: 'highlight-end'},
        },
      ],
    },
  },
};

module.exports = config;
