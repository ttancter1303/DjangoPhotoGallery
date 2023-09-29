// src/PhotoGallery.js
import React, { Component } from 'react';

class PhotoGallery extends Component {
  constructor() {
    super();
    this.state = {
      photos: [],
    };
  }

  componentDidMount() {
    // Gọi API để lấy danh sách ảnh
    fetch('http://127.0.0.1:8000/images/?format=api')
      .then((response) => response.json())
      .then((data) => this.setState({ photos: data }));
  }

  render() {
    const { photos } = this.state;

    return (
      <div className="photo-gallery">
        {photos.map((photo) => (
          <div key={photo.id} className="photo-item">
            <img src={photo.url} alt={photo.title} />
            <p>{photo.title}</p>
          </div>
        ))}
      </div>
    );
  }
}

export default PhotoGallery;
