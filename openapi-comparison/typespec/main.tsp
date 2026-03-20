import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
  title: "Library Management API",
})
@server("http://localhost:8080", "Local server")
namespace Library;

model Book {
  id: int32;
  title: string;
  author: string;
}

model BookInput {
  title: string;
  author: string;
}

@route("/books")
interface Books {
  @get
  list(): Book[];

  @post
  create(@body book: BookInput): {
    @statusCode statusCode: 201;
    @body book: Book;
  };

  @get
  @route("{id}")
  read(@path id: int32): Book;
}
