import { Component } from '@angular/core';
import { Book } from '../../models/book.model';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-form',
  templateUrl: './book-form.component.html',
  styleUrls: ['./book-form.component.css'],
})
export class BookFormComponent {
  book: Book = {
    id: 0,
    title: '',
    author: '',
    rating: 0,
  };

  constructor(private bookService: BookService) {}

  onSubmit(): void {
    this.bookService.addBook(this.book).subscribe(() => {
      // Handle success
    });
  }
}