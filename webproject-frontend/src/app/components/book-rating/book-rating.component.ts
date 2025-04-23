import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-book-rating',
  templateUrl: './book-rating.component.html',
  styleUrls: ['./book-rating.component.css'],
})
export class BookRatingComponent {
  @Input() rating: number = 0;
  @Output() ratingChange = new EventEmitter<number>();

  changeRating(newRating: number): void {
    this.rating = newRating;
    this.ratingChange.emit(newRating);
  }
}