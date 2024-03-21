import { useState } from "react";
import { getToken } from "../components/getToken";

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Use the getToken function to get the JWT token
      const token = await getToken(formData.username, formData.password);

      // Store the token securely (e.g., in a secure HTTP-only cookie or local storage)
      console.log("Received token:", token);

      // Add further logic as needed, such as redirecting to another page
    } catch (error) {
      // Handle authentication failure (e.g., display an error message)
      console.error("Authentication failed:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 border border-gray-300 rounded-md">
      <h2 className="text-2xl text-center mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-600">
            Username:
          </label>
          <input
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300"
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-600">
            Password:
          </label>
          <input
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <button
          className="w-full mt-4 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring focus:border-blue-300"
          type="submit"
        >
          Login
        </button>
      </form>
    </div>
  );
};
0
export default Login;
