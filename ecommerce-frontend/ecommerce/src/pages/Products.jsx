import React, { useEffect, useState } from "react";
import API from "../services/api";
import { Box, Button, Typography, List, ListItem } from "@mui/material";

function Products() {
  const [products, setProducts] = useState({
    results: [],
    next: null,
    previous: null,
    count: 0,
  });
  const [loading, setLoading] = useState(false);
  const [pageUrl, setPageUrl] = useState("products?page_size=2");

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const res = await API.get(pageUrl);
        console.log("Success fetching products:", res.data);
        setProducts(res.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [pageUrl]);

  const handleNext = () => {
    if (products.next) {
      // Extract relative path for API client
      const nextUrl = products.next.replace(
        "http://127.0.0.1:8000/api/v1/",
        ""
      );
      setPageUrl(nextUrl);
    }
  };

  const handlePrevious = () => {
    if (products.previous) {
      const prevUrl = products.previous.replace(
        "http://127.0.0.1:8000/api/v1/",
        ""
      );
      setPageUrl(prevUrl);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 5 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Products
      </Typography>
      {loading ? (
        <Typography>Loading...</Typography>
      ) : (
        <List>
          {products.results.map((p) => (
            <ListItem key={p.id} divider>
              {p.name} — ${p.price}
            </ListItem>
          ))}
        </List>
      )}
      <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
        <Button
          variant="contained"
          onClick={handlePrevious}
          disabled={!products.previous || loading}
        >
          Previous
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={!products.next || loading}
        >
          Next
        </Button>
      </Box>
      <Typography sx={{ mt: 2 }}>
        Showing {products.results.length} of {products.count} products
      </Typography>
    </Box>
  );
}

export default Products;
