import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [currentPage, setCurrentPage] = useState('splash');
  const [users, setUsers] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showSignupPassword, setShowSignupPassword] = useState(false);
  const [signupAllowed, setSignupAllowed] = useState(false);

  const validatePassword = (password) => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$/;
    return regex.test(password) && !password.includes(' ');
  };

  const validateAadhar = (aadhar) => {
    return /^\d{12}$/.test(aadhar);
  };

  useEffect(() => {
    fetch('http://localhost:5001/api/check-signup-allowed')
      .then(res => res.json())
      .then(data => setSignupAllowed(data.signupAllowed))
      .catch(() => setSignupAllowed(false));
  }, []);

  const handleSignup = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const userData = {
      firstName: formData.get('firstName'),
      lastName: formData.get('lastName'),
      email: formData.get('email'),
      mobile: formData.get('mobile'),
      password: formData.get('password'),
      aadhar: formData.get('aadhar')
    };

    if (!validatePassword(userData.password)) {
      alert('Password must be 8-15 characters with uppercase, lowercase, number, and special character');
      return;
    }

    if (!validateAadhar(userData.aadhar)) {
      alert('Aadhar must be exactly 12 digits');
      return;
    }

    try {
      const response = await fetch('http://localhost:5001/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      const data = await response.json();

      if (data.success) {
        alert('Account created successfully!');
        setIsSignUp(false);
        setCurrentPage('login');
      } else {
        alert('Signup failed: ' + data.error);
      }
    } catch (error) {
      alert('Error during signup. Please try again.');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const loginData = {
      emailOrUsername: formData.get('emailOrUsername'),
      password: formData.get('password')
    };

    try {
      const response = await fetch('http://localhost:5001/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
      });

      const data = await response.json();
      if (data.success) {
        window.location.href = 'http://localhost:5174/';
      } else if (data.require_totp) {
        setUsers(loginData);
        setCurrentPage('totp');
      } else {
        alert('Login failed: ' + data.error);
      }
    } catch (error) {
      alert('Error during login. Make sure backend is running.');
    }
  };

  const handleTOTP = async (e) => {
    e.preventDefault();
    const totpCode = e.target.totpCode.value;

    try {
      const response = await fetch('http://localhost:5001/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          emailOrUsername: users.emailOrUsername,
          password: users.password,
          totpCode
        })
      });

      const data = await response.json();
      if (data.success) {
        window.location.href = 'http://localhost:5174/';
        setCurrentPage('login'); // Keep state update just in case, though redirect happens
      } else {
        alert('Invalid TOTP code: ' + data.error);
      }
    } catch (error) {
      alert('Error verifying TOTP.');
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;

    if (!email) {
      alert('Please enter email address');
      return;
    }

    try {
      const response = await fetch('http://localhost:5001/api/send-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (data.success) {
        alert('OTP sent to your email! Please check your inbox.');
      } else {
        alert('Failed to send OTP: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error sending OTP. Make sure backend is running.');
    }
  };

  const handleEmailVerify = async () => {
    const email = document.querySelector('input[name="email"]').value;
    if (!email) {
      alert('Please enter email first');
      return;
    }

    try {
      const response = await fetch('http://localhost:5001/api/send-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (data.success) {
        alert('OTP sent to your email! Please check your inbox.');
      } else {
        alert('Failed to send OTP: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error sending OTP. Make sure backend is running on port 5001.');
    }
  };

  if (currentPage === 'splash') {
    return (
      <div className="splash-screen" onClick={() => setCurrentPage('login')}>
        {/* Rotating Galaxy with Trading Charts */}
        <div className="galaxy-container">
          <div className="rotating-galaxy">
            <div className="galaxy-spiral"></div>
            <div className="galaxy-core"></div>
          </div>
          <div className="stars-field">
            {[...Array(150)].map((_, i) => (
              <div key={i} className={`cosmic-star star-${i % 6}`} style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 4}s`
              }}></div>
            ))}
          </div>
          <div className="trading-overlay">
            <div className="candlestick-chart">
              {[...Array(15)].map((_, i) => (
                <div key={i} className={`candlestick ${Math.random() > 0.5 ? 'green' : 'red'}`} style={{
                  right: `${10 + i * 3}%`,
                  animationDelay: `${i * 0.2}s`
                }}>
                  <div className="wick"></div>
                  <div className="body"></div>
                </div>
              ))}
            </div>
            <div className="line-chart left">
              <svg width="250" height="80" className="chart-svg">
                <path d="M10,60 Q50,20 100,40 T200,30" stroke="#00d4ff" strokeWidth="2" fill="none" className="chart-line" />
              </svg>
            </div>
            <div className="volume-bars">
              {[...Array(12)].map((_, i) => (
                <div key={i} className="volume-bar" style={{
                  left: `${5 + i * 6}%`,
                  height: `${15 + Math.random() * 35}px`,
                  animationDelay: `${i * 0.15}s`
                }}></div>
              ))}
            </div>
          </div>
        </div>
        <div className="central-portal">
          <div className="portal-ring"></div>
          <div className="portal-core">
            <div className="bot-text">TRADING BOT</div>
          </div>
        </div>
        <div className="click-to-enter">CLICK TO INITIALIZE SYSTEM</div>
      </div>
    );
  }

  if (currentPage === 'totp') {
    return (
      <div className="totp-container">
        <div className="totp-content">
          <div className="totp-card">
            <div className="totp-header">
              <h1>Trading Bot</h1>
              <h2>Password Reset OTP</h2>
              <p>Enter the 6-digit code sent to spoorthijoshi6808@gmail.com</p>
            </div>
            <form onSubmit={handleTOTP} className="totp-form">
              <div className="totp-input-group">
                <i className="fas fa-key"></i>
                <input
                  type="text"
                  name="totpCode"
                  placeholder="000000"
                  maxLength="6"
                  className="totp-input"
                  required
                />
              </div>
              <button type="submit" className="totp-btn">VERIFY OTP</button>
            </form>
            <div className="totp-footer">
              <a href="#" onClick={() => setCurrentPage('login')}>← Back to Login</a>
            </div>
          </div>
          <div className="security-illustration">
            <div className="lock-container">
              <div className="circuit-bg">
                <div className="circuit-line line-1"></div>
                <div className="circuit-line line-2"></div>
                <div className="circuit-line line-3"></div>
                <div className="circuit-line line-4"></div>
              </div>
              <div className="lock-3d">
                <div className="lock-body">
                  <div className="lock-shackle"></div>
                  <div className="lock-keyhole">
                    <div className="keyhole-light"></div>
                  </div>
                  <div className="lock-glow"></div>
                </div>
              </div>
              <div className="sparkles">
                <div className="sparkle sparkle-1"></div>
                <div className="sparkle sparkle-2"></div>
                <div className="sparkle sparkle-3"></div>
                <div className="sparkle sparkle-4"></div>
                <div className="sparkle sparkle-5"></div>
                <div className="sparkle sparkle-6"></div>
              </div>
              <div className="light-rays">
                <div className="ray ray-1"></div>
                <div className="ray ray-2"></div>
                <div className="ray ray-3"></div>
              </div>
            </div>
            <div className="protection-text">
              <h3>RELIABLE</h3>
              <h2>PROTECTION</h2>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPage === 'forgot') {
    return (
      <div className="container">
        <div className="forgot-container">
          <h2>Forgot Password</h2>
          <p>Enter your email to receive OTP</p>
          <form onSubmit={handleForgotPassword}>
            <div className="input-group">
              <i className="fas fa-envelope"></i>
              <input type="email" name="email" placeholder="Email" required />
            </div>
            <button type="submit" className="btn-primary">Send OTP</button>
            <div className="links">
              <a href="#" onClick={() => setCurrentPage('login')}>Back to Login</a>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className={`auth-container ${isSignUp ? 'sign-up-mode' : ''}`}>
        <div className="forms-container">
          <div className="signin-signup">
            <form className="sign-in-form" onSubmit={handleLogin}>
              <h2 className="title">Login</h2>
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input type="text" name="emailOrUsername" placeholder="Username or Email" required />
              </div>
              <div className="input-field password-field">
                <i className="fas fa-lock"></i>
                <input type={showPassword ? "text" : "password"} name="password" placeholder="Password" required />
                <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'} password-toggle`} onClick={() => setShowPassword(!showPassword)}></i>
              </div>
              <input type="submit" value="Login" className="btn solid" />
              <p className="social-text">
                <a href="#" onClick={() => setCurrentPage('forgot')}>Forgot Password?</a>
              </p>
              {signupAllowed && (
                <p className="social-text">
                  Don't have an account? <a href="#" onClick={async () => {
                    try {
                      const response = await fetch('http://localhost:5001/api/check-signup-allowed');
                      const data = await response.json();
                      if (!data.signupAllowed) {
                        alert('User already exists. New signup not allowed.');
                      } else {
                        setIsSignUp(true);
                      }
                    } catch (error) {
                      setIsSignUp(true);
                    }
                  }}>Sign up</a>
                </p>
              )}
              <p className="social-text">
                <a href="http://localhost:5001/api/view-users" target="_blank" rel="noopener noreferrer">View Database Users</a>
              </p>
            </form>

            <form className="sign-up-form" onSubmit={handleSignup}>
              <h2 className="title">Sign up</h2>
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input type="text" name="firstName" placeholder="First Name" required />
              </div>
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input type="text" name="lastName" placeholder="Last Name" required />
              </div>
              <div className="input-field">
                <i className="fas fa-envelope"></i>
                <input type="email" name="email" placeholder="Email" required />
              </div>
              <div className="input-field">
                <i className="fas fa-phone"></i>
                <input type="tel" name="mobile" placeholder="Mobile Number" required />
              </div>
              <div className="input-field password-field">
                <i className="fas fa-lock"></i>
                <input type={showSignupPassword ? "text" : "password"} name="password" placeholder="Password" required />
                <i className={`fas ${showSignupPassword ? 'fa-eye-slash' : 'fa-eye'} password-toggle`} onClick={() => setShowSignupPassword(!showSignupPassword)}></i>
              </div>
              <div className="input-field">
                <i className="fas fa-id-card"></i>
                <input type="text" name="aadhar" placeholder="Aadhar Number (12 digits)" maxLength="12" pattern="[0-9]{12}" onInput={(e) => e.target.value = e.target.value.replace(/[^0-9]/g, '')} required />
              </div>
              <input type="submit" className="btn" value="Sign up" />
              <p className="social-text">
                Already have an account? <a href="#" onClick={() => setIsSignUp(false)}>Login</a>
              </p>
            </form>
          </div>
        </div>

        <div className="panels-container">
          <div className="panel left-panel">
            <div className="content">
              <div className="trading-icons">
                <div className="icon-bot">🤖</div>
                <div className="icon-chart">📈</div>
              </div>
              <h3>Welcome to Trading Bot</h3>
              <p>Advanced algorithmic trading platform with AI-powered market analysis. Secure authentication with 2FA protection. Start your automated trading journey today.</p>
              {signupAllowed && (
                <button className="btn transparent" onClick={() => setIsSignUp(true)}>Sign up</button>
              )}
            </div>
          </div>
          <div className="panel right-panel">
            <div className="content">
              <h3>One of us?</h3>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum laboriosam ad deleniti.</p>
              <button className="btn transparent" onClick={() => setIsSignUp(false)}>Sign in</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}



export default App;