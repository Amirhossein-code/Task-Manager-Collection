import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="w-full bg-gray-800 p-4 flex justify-between">
      {/* Left side - Login and Sign Up buttons */}
      <div className="flex text-white bg-black">
        <button className="hover:bg-blue-700 text-white py-2 px-4 rounded mr-4">
          Login
        </button>
        <button className="hover:bg-blue-700 text-white py-2 px-4 rounded">
          Sign Up
        </button>
      </div>

      {/* Right side - Home and About buttons */}
      <div className="flex">
        <Link to="/" className="text-white mr-4">
          <button className="hover:bg-blue-700 text-white py-2 px-4 rounded">
            Home
          </button>
        </Link>
        <Link to="/about" className="text-white">
          <button className="hover:bg-blue-700 text-white py-2 px-4 rounded">
            About
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
