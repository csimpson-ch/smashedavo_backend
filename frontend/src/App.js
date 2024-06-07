import Header from "./components/Header";
import Blog from "./components/Blog";
import DogFacts from "./components/DogFacts";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Header />} />
      <Route path="/home" element={<Header />} />
      <Route path="/blog" element={<Blog />} />
      <Route path="/dogfacts" element={<DogFacts />} />
    </Routes>
  );
}

export default App;
