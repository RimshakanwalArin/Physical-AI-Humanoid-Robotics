import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}
    >
      {/* Navigation Auth Buttons */}
      <div className={styles.authNavBar}>
        <button
          className={styles.authBtn}
          onClick={() => {
            setAuthMode('login');
            setShowAuthModal(true);
          }}
        >
          Sign In
        </button>
        <button
          className={styles.signupBtn}
          onClick={() => {
            setAuthMode('signup');
            setShowAuthModal(true);
          }}
        >
          Sign Up
        </button>
      </div>

      {/* Auth Modal */}
      {showAuthModal && (
        <div className={styles.authModal} onClick={() => setShowAuthModal(false)}>
          <div className={styles.authModalContent} onClick={(e) => e.stopPropagation()}>
            <button
              className={styles.closeBtn}
              onClick={() => setShowAuthModal(false)}
            >
              ×
            </button>
            <h2>{authMode === 'login' ? 'Welcome Back' : 'Join Us'}</h2>
            <form onSubmit={(e) => { e.preventDefault(); setShowAuthModal(false); }}>
              <input type="email" placeholder="Email" required />
              <input type="password" placeholder="Password" required />
              {authMode === 'signup' && (
                <input type="text" placeholder="Full Name" required />
              )}
              <button type="submit" className={styles.submitBtn}>
                {authMode === 'login' ? 'Sign In' : 'Create Account'}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Premium Hero Section */}
      <div className={styles.premiumHeroSection}>
        <div className={styles.premiumHeroContainer}>
          {/* Left: Animated Robot */}
          <div className={styles.robotSection}>
            <div className={styles.robotWrapper}>
              <div className={styles.robotIllustration}>
                <div className={styles.robotCore}>🤖</div>
              </div>
              {/* Decorative elements */}
              <div className={styles.floatingBall1}></div>
              <div className={styles.floatingBall2}></div>
              <div className={styles.floatingBall3}></div>
            </div>
          </div>

          {/* Right: Content Section */}
          <div className={styles.contentSection}>
            <div className={styles.contentWrapper}>
              <h1 className={styles.mainTitle}>
                Master <span className={styles.gradientText}>Physical AI</span> & Robotics
              </h1>
              {/* <p className={styles.subtitle}>
                Learn cutting-edge robotics and AI systems from industry experts. Interactive lessons, hands-on projects, and real-world applications in one comprehensive textbook.
              </p> */}

              {/* Key Stats */}
              <div className={styles.statsContainer}>
                <div className={styles.statItem}>
                  <span className={styles.statNumber}>6</span>
                  <span className={styles.statLabel}>Chapters</span>
                </div>
                <div className={styles.statItem}>
                  <span className={styles.statNumber}>100+</span>
                  <span className={styles.statLabel}>Hours</span>
                </div>
                <div className={styles.statItem}>
                  <span className={styles.statNumber}>∞</span>
                  <span className={styles.statLabel}>Learning</span>
                </div>
              </div>

              {/* CTA Buttons */}
              <div className={styles.ctaButtons}>
                <Link
                  to="/intro-physical-ai"
                  className={styles.btnPrimary}
                >
                  Start Learning Now
                </Link>
                <button
                  className={styles.btnSecondary}
                  onClick={() => {
                    setAuthMode('signup');
                    setShowAuthModal(true);
                  }}
                >
                  Create Free Account
                </button>
              </div>

              {/* Trust Badges */}
              <div className={styles.trustBadges}>
                <div className={styles.badge}>✓ AI-Powered Learning</div>
                <div className={styles.badge}>✓ Expert Instructors</div>
                <div className={styles.badge}>✓ Certificate on Completion</div>
              </div>
            </div>

            {/* Author Card - Bottom Right */}
            <div className={styles.authorCard}>
              <div className={styles.authorAvatar}>👨‍💼</div>
              <div className={styles.authorInfo}>
                <h4 className={styles.authorName}>Dr. AI Robotics</h4>
                <p className={styles.authorRole}>Course Creator</p>
              </div>
              <div className={styles.authorSocial}>
                <a href="#" className={styles.socialIcon}>f</a>
                <a href="#" className={styles.socialIcon}>t</a>
                <a href="#" className={styles.socialIcon}>in</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ padding: '0 20px' }}>
        <div style={{ margin: '80px 0', textAlign: 'center' }}>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '20px', color: '#1a202c', fontWeight: '800' }}>
            Why Choose This Textbook?
          </h2>
          <p style={{ fontSize: '1.1rem', color: '#666', marginBottom: '60px', maxWidth: '600px', margin: '0 auto 60px' }}>
            Comprehensive, interactive, and designed for real-world success
          </p>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '30px',
            maxWidth: '1200px',
            margin: '0 auto',
          }}>
            {[
              { icon: '🤖', title: 'AI-Powered Q&A ', desc: 'Chat with our intelligent tutoring system for instant answers', link:'/intro-physical-ai' },
              { icon: '📚', title: 'Complete Curriculum', desc: '6 chapters from basics to advanced robotics', link: '/humanoid-robotics' },
              { icon: '⚡', title: 'Hands-On Projects', desc: 'Build real systems with practical code examples', link: '/ros2-fundamentals' },
              { icon: '🌍', title: 'Multi-Language', desc: 'English and Urdu support for global accessibility', link: '/digital-twin-simulation' },
              { icon: '🏅', title: 'Industry Standard', desc: 'Learn tools used by top robotics companies', link: '/vision-language-action-systems' },
              { icon: '🎓', title: 'Certificate Program', desc: 'Earn certificates upon course completion', link: '/capstone-project' },
            ].map((feature, idx) => (
              <Link
                key={idx}
                to={feature.link}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div
                  style={{
                    padding: '30px',
                    borderRadius: '12px',
                    background: '#f8f9fa',
                    border: '1px solid #e2e8f0',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-8px)';
                    e.currentTarget.style.boxShadow = '0 12px 32px rgba(102, 126, 234, 0.15)';
                    e.currentTarget.style.borderColor = '#667eea';
                    e.currentTarget.style.background = '#ffffff';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = '#e2e8f0';
                    e.currentTarget.style.background = '#f8f9fa';
                  }}
                >
                  <div style={{ fontSize: '2.5rem', marginBottom: '16px' }}>{feature.icon}</div>
                  <h3 style={{ marginBottom: '12px', color: '#1a202c', fontSize: '1.2rem' }}>{feature.title}</h3>
                  <p style={{ color: '#666', margin: 0, lineHeight: '1.6' }}>{feature.desc}</p>
                  <div style={{ marginTop: '16px', color: '#667eea', fontWeight: '600', fontSize: '0.95rem' }}>
                    Learn More →
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function Home() {
  return <HomepageHeader />;
}
