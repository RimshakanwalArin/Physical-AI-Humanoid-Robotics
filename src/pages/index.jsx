import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import '../css/custom.css';

export default function Home() {
  const chapters = [
    {
      id: 1,
      icon: '🤖',
      title: 'Introduction to Physical AI',
      description: 'Learn the fundamentals of embodied intelligence and how robots perceive and interact with the physical world.',
      link: '/intro-physical-ai',
      duration: '2 hours',
      difficulty: 'Beginner',
    },
    {
      id: 2,
      icon: '🦾',
      title: 'Basics of Humanoid Robotics',
      description: 'Explore robot anatomy, sensor systems, and the mathematics of bipedal locomotion.',
      link: '/humanoid-robotics',
      duration: '3 hours',
      difficulty: 'Beginner',
    },
    {
      id: 3,
      icon: '🔄',
      title: 'ROS 2 Fundamentals',
      description: 'Master the Robot Operating System for building distributed robotic systems.',
      link: '/ros2-fundamentals',
      duration: '3 hours',
      difficulty: 'Intermediate',
    },
    {
      id: 4,
      icon: '🎮',
      title: 'Digital Twin Simulation',
      description: 'Learn to create virtual replicas of robots using Gazebo and Isaac Sim.',
      link: '/digital-twin-simulation',
      duration: '2.5 hours',
      difficulty: 'Intermediate',
    },
    {
      id: 5,
      icon: '👁️',
      title: 'Vision-Language-Action Systems',
      description: 'Integrate vision, language, and action for intelligent robotic control.',
      link: '/vision-language-action-systems',
      duration: '3 hours',
      difficulty: 'Advanced',
    },
    {
      id: 6,
      icon: '🏆',
      title: 'Capstone Project',
      description: 'Build an end-to-end AI system for household task robotics.',
      link: '/capstone-project',
      duration: '4 hours',
      difficulty: 'Advanced',
    },
  ];

  return (
    <Layout
      title="Physical AI & Humanoid Robotics Textbook"
      description="Learn AI-powered robotics with an interactive, intelligent textbook"
    >
      {/* Hero Section */}
      <div style={{ padding: '0 20px' }}>
        <div className="hero" style={{ marginTop: '40px' }}>
          <h1>🚀 Physical AI & Humanoid Robotics</h1>
          <p>
            A comprehensive, AI-powered textbook for learning intelligent robotic systems
            from fundamentals to advanced applications.
          </p>
          <div style={{ marginTop: '30px', display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link
              className="button button--primary"
              style={{
                padding: '12px 24px',
                fontSize: '1rem',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.2)',
                border: '2px solid white',
                color: 'white',
                textDecoration: 'none',
                fontWeight: '600',
                transition: 'all 0.3s ease',
              }}
              to="/intro-physical-ai"
            >
              Start Learning →
            </Link>
          </div>
        </div>

        {/* Features */}
        <div style={{ margin: '60px 0', textAlign: 'center' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '40px', color: '#1a202c' }}>
            Why Choose This Textbook?
          </h2>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '24px',
              maxWidth: '1200px',
              margin: '0 auto',
            }}
          >
            {[
              { icon: '🤖', title: 'AI-Powered Learning', desc: 'Interactive RAG chatbot answers your questions with citations' },
              { icon: '📚', title: 'Comprehensive Content', desc: '6 chapters covering fundamentals to advanced topics' },
              { icon: '⚡', title: 'Hands-On Projects', desc: 'Build real systems with practical code examples' },
              { icon: '🌍', title: 'Multi-Language', desc: 'English and Urdu support for global accessibility' },
            ].map((feature, idx) => (
              <div
                key={idx}
                style={{
                  padding: '24px',
                  borderRadius: '12px',
                  background: '#f8f9fa',
                  border: '1px solid #e2e8f0',
                  transition: 'all 0.3s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-8px)';
                  e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>{feature.icon}</div>
                <h3 style={{ marginBottom: '8px', color: '#1a202c' }}>{feature.title}</h3>
                <p style={{ color: '#4a5568', margin: 0 }}>{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Chapters Grid */}
        <div style={{ margin: '80px 0' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '40px', textAlign: 'center', color: '#1a202c' }}>
            Course Chapters
          </h2>
          <div className="chapters-grid">
            {chapters.map((chapter) => (
              <Link
                key={chapter.id}
                to={chapter.link}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="chapter-card">
                  <div className="chapter-card-icon">{chapter.icon}</div>
                  <h3 className="chapter-card-title">{chapter.title}</h3>
                  <p className="chapter-card-description">{chapter.description}</p>
                  <div className="chapter-card-meta">
                    <span>⏱️ {chapter.duration}</span>
                    <span>📊 {chapter.difficulty}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '60px 24px',
            borderRadius: '12px',
            textAlign: 'center',
            marginBottom: '80px',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
          }}
        >
          <h2 style={{ fontSize: '2rem', marginBottom: '16px' }}>Ready to Master Robotics AI?</h2>
          <p style={{ fontSize: '1.1rem', marginBottom: '30px', opacity: 0.95 }}>
            Start with the basics or jump to advanced topics. Learn at your own pace with our interactive textbook.
          </p>
          <Link
            className="button"
            style={{
              padding: '14px 28px',
              fontSize: '1rem',
              borderRadius: '8px',
              background: 'white',
              color: '#667eea',
              textDecoration: 'none',
              fontWeight: '700',
              transition: 'all 0.3s ease',
              display: 'inline-block',
            }}
            to="/intro-physical-ai"
          >
            Explore Chapters
          </Link>
        </div>
      </div>
    </Layout>
  );
}
