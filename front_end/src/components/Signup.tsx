import React, { useState } from 'react';
import { Button, FormGroup, InputGroup, Card, Classes, Callout } from '@blueprintjs/core';
import axios from 'axios'

const Signup: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const handleSignup = async () => {
    if (password !== confirmPassword) {
      setError("both passwords are different");
    }
    else {
      setError("")
      try {
        const response = await axios.post('/backend/api/user', { username, email, password });
        console.log("hola")
        console.log("Signup successful", response.data);
      } catch (error) {
        console.log("Signup failed", error);
      }
    }
  }
  return (
    <div className="signup-container">
      <Card style={{ maxWidth: '400px', margin: '0 auto', padding: '50px', backgroundColor: '#f4f4f4' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#357CB6' }}>Signup</h2>
        {error && <Callout style={{ color: 'red', marginBottom: "10px" }} intent="danger">{error}</Callout>}
        <FormGroup label="Username" labelFor="username-input" style={{ marginBottom: '15px' }}>
          <InputGroup
            id="username-input"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </FormGroup>
        <FormGroup label="Email" labelFor="email-input" style={{ marginBottom: '15px' }}>
          <InputGroup
            id="email-input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormGroup>
        <FormGroup label="Password" labelFor="password-input" style={{ marginBottom: '15px' }}>
          <InputGroup
            id="password-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormGroup>
        <FormGroup label="Confirm Password" labelFor="confirm-password-input" style={{ marginBottom: '15px' }}>
          <InputGroup
            id="confirm-password-input"
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </FormGroup>
        <Button
          intent="primary"
          onClick={handleSignup}
          style={{ width: '100%', marginTop: '20px', backgroundColor: '#357CB6' }}
        >
          Sign Up
        </Button>
      </Card>
    </div>
  );
};

export default Signup;
