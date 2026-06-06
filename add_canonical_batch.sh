#!/bin/bash
# Batch add canonical tags to all HTML guide files
# Usage: bash add_canonical_batch.sh

GUIDES_DIR="C:/Users/Lenovo/osrs-guide-site/guides"
BASE_URL="https://osrsguru.com/guides"

# Find all HTML files missing canonical tag
for file in "$GUIDES_DIR"/*.html; do
    # Skip if already has canonical tag
    if grep -q 'rel="canonical"' "$file" 2>/dev/null; then
        echo "SKIP (already has canonical): $(basename "$file")"
        continue
    fi
    
    filename=$(basename "$file")
    canonical_url="$BASE_URL/$filename"
    
    # Insert canonical link after <meta name="keywords" ...>
    # Using sed to insert the line after the keywords meta tag
    sed -i '/<meta name="keywords"/a\    <link rel="canonical" href="'"$canonical_url"'">' "$file"
    
    if [ $? -eq 0 ]; then
        echo "ADDED: $filename"
    else
        echo "ERROR: $filename"
    fi
done

echo ""
echo "Done! Checking results..."
grep -L "rel=\"canonical\"" "$GUIDES_DIR"/*.html 2>/dev/null || echo "All files now have canonical tags!"
