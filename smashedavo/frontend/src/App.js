import Header from "./components/Header";
import Login from "./components/Login";
import BlogPosts from "./components/BlogPosts";
import Expenses from "./components/Expenses";
import { Routes, Route } from "react-router-dom";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Header />} />
      <Route path="/login" element={<Login />} />
      <Route path="/blog" element={<BlogPosts />} />
      <Route path="/expenses" element={<Expenses />} />
    </Routes>
  );
}

export default App;
