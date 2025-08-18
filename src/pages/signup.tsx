// src/pages/Signup.tsx
import React from "react";

const Signup: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-2">Sign Up</h2>
        <p className="text-gray-600 text-center mb-6">
          Please fill in this form to create an account!
        </p>

        <form>
          {/* First & Last Name */}
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="First Name"
              className="w-1/2 p-2 border border-gray-300 rounded"
            />
            <input
              type="text"
              placeholder="Last Name"
              className="w-1/2 p-2 border border-gray-300 rounded"
            />
          </div>

          {/* Email */}
          <input
            type="email"
            placeholder="Email"
            className="w-full p-2 border border-gray-300 rounded mb-4"
          />

          {/* Password */}
          <input
            type="password"
            placeholder="Password"
            className="w-full p-2 border border-gray-300 rounded mb-4"
          />

          {/* Confirm Password */}
          <input
            type="password"
            placeholder="Confirm Password"
            className="w-full p-2 border border-gray-300 rounded mb-4"
          />

          {/* Terms & Conditions */}
          <div className="flex items-center mb-4 text-sm">
            <input type="checkbox" className="mr-2" />
            <span>
              I accept the{" "}
              <a href="#" className="text-blue-500 underline">
                Terms of Use
              </a>{" "}
              &{" "}
              <a href="#" className="text-blue-500 underline">
                Privacy Policy
              </a>
            </span>
          </div>

          {/* Sign Up Button */}
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white p-2 rounded"
          >
            Sign Up
          </button>
        </form>

        {/* Already have an account */}
        <p className="text-center text-sm mt-4">
          Already have an account?{" "}
          <a href="#" className="text-blue-500 underline">
            Login here
          </a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
